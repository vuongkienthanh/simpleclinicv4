import wx
import sqlite3
from lib.vn import wxdatetime_to_vietnamese_datetime
from lib.wx_helper import get_main_frame


class List(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("Mã lượt khám", width=-1)
        self.AppendColumn("Ngày giờ khám", width=200)
        self.AppendColumn("Chẩn đoán", width=250)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_visit_select)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_visit_deselect)

    def append(self, item: sqlite3.Row):
        self.Append(
            [
                str(item["id"]),
                wxdatetime_to_vietnamese_datetime(item["exam_datetime"]),
                item["diagnosis"],
            ]
        )

    def on_visit_select(self, e: wx.ListEvent):
        get_main_frame().visit_id = int(self.GetItemText(e.Index, 0))

    def on_visit_deselect(self, _):
        get_main_frame().visit_id = None
