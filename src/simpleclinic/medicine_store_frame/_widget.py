import wx
import sqlite3
from lib.wx_helper import lc_scale


class List(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("Mã", width=lc_scale(50))
        self.AppendColumn("Tên", width=lc_scale(250))
        self.AppendColumn("Thành phần", width=lc_scale(250))
        self.AppendColumn("Số lượng", width=lc_scale(100))
        self.AppendColumn("Đường dùng", width=lc_scale(100))
        self.AppendColumn("Đơn vị dùng", width=lc_scale(100))
        self.AppendColumn("Đơn vị bán", width=lc_scale(100))
        self.AppendColumn("Giá mua", width=lc_scale(100))
        self.AppendColumn("Giá bán", width=lc_scale(100))

    def append(self, item: sqlite3.Row):
        self.Append(
            [
                str(item["id"]),
                item["name"],
                item["element"],
                str(item["quantity"]),
                item["route"],
                item["usage_unit"],
                item["selling_unit"],
                item["cost_price"],
                item["selling_price"],
            ]
        )
