import wx
import sqlite3
from lib.db import DATE_FORMAT
from lib.wx_helper import get_main_frame
from collections.abc import Mapping
from typing import Any


class ListCtrl(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("Mã BN", width=-1)
        self.AppendColumn("Tên", width=300)
        self.AppendColumn("Giới", width=-2)
        self.AppendColumn("Ngày sinh", width=-2)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_deselect)

    def append(self, item: sqlite3.Row | Mapping[str, Any]):
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

    def on_deselect(self, _: wx.ListEvent):
        get_main_frame().patient_id = None


class Book(wx.Notebook):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self.queue = ListCtrl(self)
        self.seentoday = ListCtrl(self)
        self.appointment = ListCtrl(self)
        self.AddPage(page=self.queue, text="Danh sách BN", select=True)
        self.AddPage(page=self.seentoday, text="Đã khám hôm nay")
        self.AddPage(page=self.appointment, text="Tái khám")
