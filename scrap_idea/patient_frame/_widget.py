import wx
import sqlite3


class ListCtrl(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("Mã", width=-1)
        self.AppendColumn("Tên", width=-1)
        self.AppendColumn("Giới", width=-1)
        self.AppendColumn("Ngày sinh", width=-1)

    def append(self, item: sqlite3.Row):
        self.Append(
            [
                str(item["id"]),
                item["name"],
                item["gender"].display_name,
                item["birthdate"].Format("%d/%m/%Y"),
            ]
        )
