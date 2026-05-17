import wx
import sqlite3


class List(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("Mã", width=-1)
        self.AppendColumn("Tên", width=-1)
        self.AppendColumn("Thành phần", width=-1)
        self.AppendColumn("Số lượng", width=-1)
        self.AppendColumn("Đường dùng", width=-1)
        self.AppendColumn("Đơn vị dùng", width=-1)
        self.AppendColumn("Đơn vị bán", width=-1)
        self.AppendColumn("Giá mua", width=-1)
        self.AppendColumn("Giá bán", width=-1)

    def append(self, item: sqlite3.Row):
        self.Append(
            [
                str(item["id"]),
                item["name"],
                item["element"],
                str(item["quantity"]),
                item["route"],
                item["usage_unit"],
                item["sale_unit"],
                item["cost_price"],
                item["selling_price"],
            ]
        )
