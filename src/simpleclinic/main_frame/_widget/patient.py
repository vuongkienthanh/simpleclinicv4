import wx
import sqlite3
from lib import DATE_FORMAT
from lib.wx_helper import get_main_frame


class List(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("Mã BN", width=-1)
        self.AppendColumn("Tên", width=300)
        self.AppendColumn("Giới", width=-2)
        self.AppendColumn("Ngày sinh", width=150)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_patient_select)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_patient_deselect)

    def append(self, item: sqlite3.Row):
        self.Append(
            [
                str(item["id"]),
                item["name"],
                item["gender"].display_name,
                item["birthdate"].Format(DATE_FORMAT),
            ]
        )

    def on_patient_select(self, e: wx.ListEvent):
        get_main_frame().patient_id = int(self.GetItemText(e.Index, 0))

    def on_patient_deselect(self, _):
        get_main_frame().patient_id = None
