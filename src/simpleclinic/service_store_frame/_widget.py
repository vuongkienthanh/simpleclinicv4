import wx
import sqlite3
from lib.wx_helper import lc_scale


class List(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("Mã", width=lc_scale(50))
        self.AppendColumn("Tên", width=lc_scale(250))
        self.AppendColumn("Giá", width=lc_scale(100))

    def append(self, item: sqlite3.Row):
        self.Append(
            [
                str(item["id"]),
                item["name"],
                str(item["selling_price"]),
            ]
        )
