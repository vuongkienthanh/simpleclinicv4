import wx
import sqlite3
from lib import DATE_FORMAT


class List(wx.ListCtrl):
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
