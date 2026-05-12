from typing import Any
import wx
import sqlite3
from collections.abc import Mapping


class List(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("Mã", width=-1)
        self.AppendColumn("Tên", width=-1)
        self.AppendColumn("Giá", width=-1)

    def append(self, item: sqlite3.Row | Mapping[str, Any]):
        self.Append(
            [
                str(item["id"]),
                item["name"],
                str(item["price"]),
            ]
        )
