from concurrent.interpreters import get_main

import wx
import sqlite3
from lib import DATE_FORMAT
from lib.wx_helper import get_main_frame


class List(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("Mã BN", width=-1)
        self.AppendColumn("Tên", width=280)
        self.AppendColumn("Giới", width=-2)
        self.AppendColumn("Ngày sinh", width=130)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_click)

    def append(self, item: sqlite3.Row):
        self.Append(
            [
                str(item["id"]),
                item["name"],
                item["gender"].display_name,
                item["birthdate"].Format(DATE_FORMAT),
            ]
        )

    def on_select(self, e: wx.ListEvent):
        get_main_frame().patient_id = int(self.GetItemText(e.Index, 0))

    def on_left_click(self, e: wx.MouseEvent):
        pos = e.GetPosition()
        index, _ = self.HitTest(pos)
        if index == wx.NOT_FOUND:
            current_selected = self.GetFirstSelected()
            if current_selected != -1:
                self.Select(current_selected, on=False)
            get_main_frame().patient_id = None
        e.Skip()


class Queue(List):
    def query(self, value: str):
        self.DeleteAllItems()
        for item in get_app().conn.execute(
            """
            SELECT id, name, gender, birthdate from patients
            WHERE name LIKE ?
            """,
            ("%" + value.upper() + "%",),
        ):
            self.append(item)


class SeenToday(List):
    def query(self):
        self.DeleteAllItems()
        for item in get_app().conn.execute("SELECT * FROM seen_today"):
            self.append(item)


class FollowUp(List):
    def query(self):
        self.DeleteAllItems()
        for item in get_app().conn.execute("SELECT * FROM follow_up"):
            self.append(item)