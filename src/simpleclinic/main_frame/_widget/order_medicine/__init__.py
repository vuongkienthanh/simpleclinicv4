import wx
from wx.lib.intctrl import IntCtrl
from wx.lib.masked.numctrl import NumCtrl
from lib.paths import MINUS_BM, PLUS_BM
from lib.wx_helper import (
    row,
    EA,
    NUMBERS,
    NUMPADS,
    SPECIALS,
    SLASH,
    DECIMAL,
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
        self.times = IntCtrl(self, min=0, limited=True)
        self.dose = DoseCtrl(self)
        self.usage_unit = wx.StaticText(self, label="{đơn vị}")
        self.quantity = IntCtrl(self, min=0, limited=True)
        self.selling_unit = wx.StaticText(self, label="{đơn vị}")
        self.usage_note = wx.TextCtrl(self)
        self.price = NumCtrl(self, style=wx.TE_READONLY)
        self.price.SetParameters(groupDigits=True, groupChar=".", decimalChar=",")
        self.list = List(self)
        self.addbtn = wx.BitmapButton(
            self, bitmap=wx.BitmapBundle(wx.Bitmap(str(PLUS_BM)))
        )
        self.delbtn = wx.BitmapButton(
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
            static("Thuốc: ", 100),
            (self.search, 1, EA, 2),
            static("Ngày "),
            (self.times, 0, EA, 2),
            static("lần, lần"),
            (self.dose, 0, EA, 2),
            (self.usage_unit, 0, wx.ALIGN_CENTER_VERTICAL, 2),
            static("Tổng: "),
            (self.quantity, 0, EA, 2),
            (self.selling_unit, 0, wx.ALIGN_CENTER_VERTICAL, 2),
            (self.addbtn, 0, EA, 2),
            (self.delbtn, 0, EA, 2),
        )
        row2 = row(
            static("Cách sử dụng:", 120),
            (self.usage_note, 1, EA, 2),
            static("Đơn giá: "),
            (self.price, 0, EA, 2),
        )
        self.SetSizerAndFit(
            column((row1, 0, EA, 5), (row2, 0, EA, 5), (self.list, 1, EA, 5))
        )


class DoseCtrl(wx.TextCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self.Bind(wx.EVT_CHAR, self.on_char)

    def on_char(self, e: wx.KeyEvent):
        keys = NUMBERS + NUMPADS + SPECIALS
        s = self.Value
        if "/" not in s and "." not in s:
            keys += SLASH + DECIMAL

        if e.KeyCode in keys:
            e.Skip()


class List(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("STT", width=-1)
        self.AppendColumn("Mã", width=-1)
        self.AppendColumn("Thuốc", width=-1)
        self.AppendColumn("Thành phần", width=-1)
        self.AppendColumn("Số Lần", width=-1)
        self.AppendColumn("Mỗi lần", width=-1)
        self.AppendColumn("Số lượng", width=-1)
        self.AppendColumn("Cách sử dụng", width=300)
        self.AppendColumn("Giá", width=-1)

    def append(self, item: sqlite3.Row | Mapping[str, Any]):
        self.Append(
            [
                str(self.GetItemCount() + 1),
                str(item["id"]),
                item["name"],
                item["element"],
                str(item["times"]),
                f"{item['dose']} {item['usage_unit']}",
                f"{item['quantity']} {item['selling_unit']}",
                item["usage_note"],
                str(item["price"] * item["quantity"]),
            ]
        )
