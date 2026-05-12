import wx
import sqlite3
from collections.abc import Mapping
from typing import Any


class List(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("Mã lượt khám", width=-2)
        self.AppendColumn("Ngày giờ khám", width=-2)
        self.AppendColumn("Chẩn đoán", width=-2)

    def append(self, item: sqlite3.Row | Mapping[str, Any]):
        self.Append(
            [
                str(item["id"]),
                item["exam_datetime"],
                item["diagnosis"],
            ]
        )
