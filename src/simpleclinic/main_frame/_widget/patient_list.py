import wx
import sqlite3
from lib.db import DATE_FORMAT


class ListCtrl(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("Mã BN", width=-1)
        self.AppendColumn("Tên", width=300)
        self.AppendColumn("Giới", width=-2)
        self.AppendColumn("Ngày sinh", width=-2)

    def append(self, item: sqlite3.Row):
        self.Append(
            [
                str(item["id"]),
                item["name"],
                item["gender"].display_name,
                item["birthdate"].Format(DATE_FORMAT),
            ]
        )


class BookCtrl(wx.Notebook):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self.queue = ListCtrl(self)
        self.seentoday = ListCtrl(self)
        self.AddPage(page=self.queue, text="Danh sách BN", select=True)
        self.AddPage(page=self.seentoday, text="Đã khám hôm nay")
