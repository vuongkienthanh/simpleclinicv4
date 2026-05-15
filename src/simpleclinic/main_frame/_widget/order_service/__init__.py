import wx
from lib.paths import MINUS_BM, PLUS_BM
from wx.lib.intctrl import IntCtrl
from wx.lib.masked.numctrl import NumCtrl
from lib.wx_helper import (
    row,
    EA,
    column,
    get_app,
)
import sqlite3
from collections.abc import Mapping
from typing import Any
from .comboctrl import Picker


class Panel(wx.Panel):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self.SetBackgroundColour(wx.Colour(*get_app().config["theme"]["order_info"]))
        self.search = Picker(self)
        self.quantity = IntCtrl(self, min=0, limited=True)
        self.price = NumCtrl(self, style=wx.TE_READONLY)
        self.price.SetGroupDigits(True)
        self.price.SetParameters(groupDigits=True, groupChar=".", decimalChar=",")
        self.list = List(self)
        self.add_btn = wx.BitmapButton(
            self, bitmap=wx.BitmapBundle(wx.Bitmap(str(PLUS_BM)))
        )
        self.del_btn = wx.BitmapButton(
            self, bitmap=wx.BitmapBundle(wx.Bitmap(str(MINUS_BM)))
        )

        def static(label, width=-1):
            return (
                wx.StaticText(self, label=label, size=wx.Size(width, -1)),
                0,
                wx.ALIGN_CENTER_VERTICAL,
                0,
            )

        row1 = row(
            static("Dịch vụ: ", 100),
            (self.search, 1, EA, 2),
            static("Tổng: "),
            (self.quantity, 0, EA, 2),
            static("Đơn giá: "),
            (self.price, 0, EA, 2),
            (self.add_btn, 0, EA, 2),
            (self.del_btn, 0, EA, 2),
        )
        self.SetSizerAndFit(column((row1, 0, EA, 5), (self.list, 1, EA, 5)))


class List(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("STT", width=-1)
        self.AppendColumn("Mã", width=-1)
        self.AppendColumn("Dịch vụ", width=-1)
        self.AppendColumn("Số lượng", width=-1)
        self.AppendColumn("Giá", width=-1)

    def append(self, item: sqlite3.Row | Mapping[str, Any]):
        self.Append(
            [
                str(self.GetItemCount() + 1),
                str(item["id"]),
                item["name"],
                str(item["quantity"]),
                str(item["price"] * item["quantity"]),
            ]
        )
