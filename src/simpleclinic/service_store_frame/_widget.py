import wx
import sqlite3


class List(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("Mã", width=-1)
        self.AppendColumn("Tên", width=300)
        self.AppendColumn("Giá", width=-1)

    def append(self, item: sqlite3.Row):
        self.Append(
            [
                str(item["id"]),
                item["name"],
                str(item["selling_price"]),
            ]
        )
