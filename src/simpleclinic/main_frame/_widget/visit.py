import wx
import sqlite3
from lib.vn import wxdatetime_to_vietnamese


class List(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("Mã lượt khám", width=-2)
        self.AppendColumn("Ngày giờ khám", width=200)
        self.AppendColumn("Chẩn đoán", width=300)

    def append(self, item: sqlite3.Row):
        self.Append(
            [
                str(item["id"]),
                wxdatetime_to_vietnamese(item["exam_datetime"]),
                item["diagnosis"],
            ]
        )
