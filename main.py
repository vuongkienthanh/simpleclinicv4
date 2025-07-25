import os
import os.path
import sys
from sqlite3 import Connection

import wx

import database
from paths import DB_PATH


class App(wx.App):
    def __init__(self, con: Connection):
        super().__init__()
        from app.mainview import MainView

        mv = MainView(con)
        self.SetTopWindow(mv)
        self.MainLoop()


def platform_settings():
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    elif sys.platform == "linux":
        # light theme
        os.environ["GTK_THEME"] = "Default " + os.path.abspath(__file__)
        pass


if __name__ == "__main__":
    con = database.Connection(DB_PATH)
    platform_settings()
    App(con)
