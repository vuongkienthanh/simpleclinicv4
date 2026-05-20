import sqlite3
import tomllib
import wx
from lib.paths import DB_PATH, CFG_PATH, PYPROJECT, START_APP_SQL, CLOSE_APP_SQL
from lib.config import get_config
from lib.db import connect
from lib.wx_helper import get_main_frame
import sys
import os
from typing import override
from .main_frame import MainFrame as MainFrame


def platform_settings():
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    elif sys.platform == "linux":
        # light theme
        os.environ["GTK_THEME"] = "Default " + os.path.abspath(__file__)


class App(wx.App):
    def __init__(self):
        super().__init__()
        self.locale = wx.Locale(wx.LANGUAGE_VIETNAMESE)
        with open(PYPROJECT, "rb") as f:
            data = tomllib.load(f)
            self.SetAppName(data["project"]["name"])
            self.SetAppDisplayName(data["project"]["description"])
            self.SetVendorName(data["project"]["authors"][0]["name"])
            self.SetVendorDisplayName(data["project"]["authors"][0]["email"])
            self.version = data["project"]["version"]
            self.description = data["project"]["description"]

        self.config = get_config()
        self.conn = connect(DB_PATH)

        # CREATE TRIGGERS at start
        with open(START_APP_SQL, "r") as f:
            self.conn.executescript(f.read())

        main_frame = MainFrame()
        main_frame.Show()
        self.SetTopWindow(main_frame)

        # DATA
        self.medicine_store: list[sqlite3.Row]
        self.service_store: list[sqlite3.Row]
        self.fetch_stable_data()

        main_frame.patient_id = None
        main_frame.visit_id = None
        main_frame.medicine = None
        main_frame.service = None

    @override
    def __del__(self):
        with open(CLOSE_APP_SQL, "r") as f:
            self.conn.executescript(f.read())
        self.conn.close()
        super().__del__()

    def fetch_medicine_store(self):
        self.medicine_store = self.conn.execute("""
            SELECT id, name, element, quantity, route, usage_unit, selling_unit, cost_price, selling_price
            FROM medicine_store
        """).fetchall()

    def fetch_service_store(self):
        self.service_store = self.conn.execute("""
            SELECT id, name, price
            FROM service_store
        """).fetchall()

    def fetch_stable_data(self):
        self.fetch_medicine_store()
        self.fetch_service_store()

    def refresh(self):
        self.fetch_stable_data()
        get_main_frame().refresh()


def main():
    print("Checking health:... ", end="")
    assert DB_PATH.exists(), "should have a database"
    assert CFG_PATH.exists(), "should have a config file"
    print("Done")

    platform_settings()
    App().MainLoop()
