import wx
import sqlite3
from typing import override
from lib.wx_helper import get_app, get_main_frame


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

    def append(self, item: sqlite3.Row):
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


class Popup(wx.ComboPopup):
    def __init__(self):
        super().__init__()
        self.lc: wx.ListCtrl
        self.curitem: int

    @override
    def Create(self, parent):
        self.lc = wx.ListCtrl(
            parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER
        )
        self.lc.AppendColumn("Mã", width=-1)
        self.lc.AppendColumn("Thuốc", width=-1)
        self.lc.AppendColumn("Thành phần", width=-1)
        self.lc.AppendColumn("Số lượng", width=-1)
        self.lc.AppendColumn("Đơn vị", width=-1)
        self.lc.AppendColumn("Đơn giá", width=-1)
        self.lc.AppendColumn("Cách dùng", width=-1)
        self.lc.Bind(wx.EVT_MOTION, self.on_motion)
        self.lc.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.lc.Bind(wx.EVT_CHAR, self.on_char)
        return True

    @override
    def GetControl(self):
        return self.lc

    @override
    def Init(self):
        self.curitem = -1

    @override
    def GetStringValue(self) -> str:
        return ""

    @override
    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return wx.ComboPopup.GetAdjustedSize(self, 600, 200, 400)

    @override
    def OnPopup(self):
        s: str = self.ComboCtrl.Value
        self.lc.DeleteAllItems()
        s = s.strip().casefold()
        for item in filter(
            lambda item: (
                (s in item["name"].casefold()) or (s in item["element"].casefold())
            ),
            get_app().medicine_store,
        ):
            self.lc.Append(
                [
                    item["id"],
                    item["name"],
                    item["element"],
                    item["quantity"],
                    item["selling_unit"],
                    item["selling_price"],
                    item["route"],
                ]
            )

    def on_motion(self, e):
        index, _ = self.lc.HitTest(e.GetPosition())
        if index >= 0:
            self.lc.Select(index)
            self.curitem = index

    def on_left_down(self, _):
        if self.curitem >= 0:
            self.select_drug()

    def select_drug(self):
        cc = self.ComboCtrl
        i = self.curitem
        get_main_frame().medicine_id = int(self.lc.GetItemText(i, 0))
        cc.Value = self.lc.GetItemText(i, 1)
        self.Dismiss()
        cc.Navigate()

    def on_char(self, e: wx.KeyEvent):
        c = e.KeyCode
        if c == wx.WXK_DOWN:
            if self.lc.ItemCount > 0:
                if self.curitem < (self.lc.ItemCount - 1):
                    self.curitem += 1
                self.lc.Select(self.curitem)
                self.lc.EnsureVisible(self.curitem)
        elif c == wx.WXK_UP:
            if self.lc.ItemCount > 0:
                if self.curitem > 0:
                    self.curitem -= 1
                self.lc.Select(self.curitem)
                self.lc.EnsureVisible(self.curitem)
        elif c == wx.WXK_ESCAPE:
            self.Dismiss()
        elif c == wx.WXK_RETURN:
            if self.lc.ItemCount > 0:
                self.select_drug()


class Picker(wx.ComboCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.TE_PROCESS_ENTER)
        self.SetPopupControl(Popup())
        self.Bind(wx.EVT_CHAR, self.on_char)
        self.SetHint("Enter để search thuốc")

    def on_char(self, e: wx.KeyEvent):
        if e.KeyCode == wx.WXK_RETURN:
            self.Popup()
        else:
            e.Skip()
