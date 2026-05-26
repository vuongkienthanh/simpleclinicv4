from collections.abc import Iterable
import wx
import sqlite3
from typing import override
from lib.wx_helper import get_app, get_main_frame
from lib.db.models import Medicine


class List(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("STT", width=-1)
        self.AppendColumn("Mã thuốc", width=-1)
        self.AppendColumn("Thuốc", width=200)
        self.AppendColumn("Thành phần", width=-1)
        self.AppendColumn("Cách dùng", width=-1)
        self.AppendColumn("Số Lần", width=-1)
        self.AppendColumn("Mỗi lần", width=-1)
        self.AppendColumn("Số lượng", width=-1)
        self.AppendColumn("Ghi chú", width=-1)
        self.AppendColumn("Giá", width=-1)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_medicine_list_select)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_medicine_list_deselect)

    def append(self, item: sqlite3.Row):
        self.Append(
            [
                str(self.GetItemCount() + 1),
                item["id"],
                item["name"],
                item["element"],
                item["route"],
                str(item["times"]),
                f"{item['dose']} {item['usage_unit']}",
                f"{item['quantity']} {item['selling_unit']}",
                item["usage_note"],
                str(item["selling_price"] * item["quantity"]),
            ]
        )

    def on_medicine_list_select(self, e: wx.ListEvent):
        medicine_id = int(self.GetItemText(e.Index, 1))
        for i, m in enumerate(get_app().medicine_store):
            if m["id"] == medicine_id:
                get_main_frame().medicine = get_app().medicine_store[i]
                break
        get_main_frame().medicine_times.ChangeValue(int(self.GetItemText(e.Index, 3)))  # pyright: ignore[reportArgumentType]
        get_main_frame().medicine_dose.ChangeValue(self.GetItemText(e.Index, 4))
        get_main_frame().medicine_quantity.ChangeValue(
            int(self.GetItemText(e.Index, 5))  # pyright: ignore[reportArgumentType]
        )
        get_main_frame().medicine_usage_note.ChangeValue(self.GetItemText(e.Index, 6))
        get_main_frame().display_usage_note()

    def on_medicine_list_deselect(self, _):
        get_main_frame().medicine = None

    def to_model(self) -> Iterable[Medicine]:
        visit_id = get_main_frame().visit_id
        assert visit_id is not None
        for i in range(self.ItemCount):
            yield Medicine(
                medicine_id=int(self.GetItemText(i, 1)),
                visit_id=visit_id,
                times=int(self.GetItemText(i, 5)),
                dose=self.GetItemText(i, 6).split(" ", 1)[0],
                quantity=int(self.GetItemText(i, 7).split(" ", 1)[0]),
                usage_note=self.GetItemText(i, 8),
            )


class Popup(wx.ComboPopup):
    def __init__(self):
        super().__init__()
        self.lc: wx.ListCtrl
        self._ptr_list: list[int] = []
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
        self.curitem = -1
        self.lc.DeleteAllItems()
        self._ptr_list.clear()
        s = s.strip().casefold()
        for i, item in filter(
            lambda elem: (
                (s in elem[1]["name"].casefold())
                or (s in elem[1]["element"].casefold())
            ),
            enumerate(get_app().medicine_store),
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
            self._ptr_list.append(i)

    def on_motion(self, e):
        index, _ = self.lc.HitTest(e.GetPosition())
        if index >= 0:
            self.lc.Select(index)
            self.curitem = index

    def on_left_down(self, _):
        if self.curitem >= 0:
            self.select_item()

    def select_item(self):
        get_main_frame().medicine = get_app().medicine_store[
            self._ptr_list[self.curitem]
        ]
        self.Dismiss()
        self.ComboCtrl.Navigate()
        get_main_frame().medicine_del_btn.Disable()

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
                self.select_item()


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
