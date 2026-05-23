import sqlite3
import wx
from ._widget import List
from simpleclinic.service_dialog import AddDialog, UpdateDialog
from lib.wx_helper import EA, row, column, get_app
from lib.db import delete
from lib.db.models import ServiceStore


class StoreFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Dịch vụ")
        self.Maximize()
        self.searchctrl = wx.SearchCtrl(self)
        self.listctrl = List(self)
        self.add_btn = wx.Button(self, label="Thêm mới")
        self.upd_btn = wx.Button(self, label="Cập nhật")
        self.del_btn = wx.Button(self, label="Xoá")

        search_sizer = row(
            (wx.StaticText(self, label="Tìm kiếm"), 0, wx.ALL | wx.ALIGN_CENTER, 5),
            (self.searchctrl, 1, EA, 5),
        )
        btn_sizer = row(
            (0, 0, 1),
            (self.add_btn, 0, wx.RIGHT, 5),
            (self.upd_btn, 0, wx.RIGHT, 5),
            (self.del_btn, 0, wx.RIGHT, 5),
        )
        self.SetSizerAndFit(
            column(
                (search_sizer, 0, EA, 5),
                (self.listctrl, 1, EA, 5),
                (btn_sizer, 0, EA, 5),
            )
        )

        self.refresh()

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_SEARCH, self.on_search, source=self.searchctrl)
        self.Bind(wx.EVT_TEXT, self.on_text, source=self.searchctrl)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select, source=self.listctrl)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_deselect, source=self.listctrl)
        self.Bind(wx.EVT_BUTTON, self.on_add, source=self.add_btn)
        self.Bind(wx.EVT_BUTTON, self.on_upd, source=self.upd_btn)
        self.Bind(wx.EVT_BUTTON, self.on_del, source=self.del_btn)

    def refresh(self):
        self.searchctrl.ChangeValue("")
        self.listctrl.DeleteAllItems()
        for item in get_app().service_store:
            self.listctrl.append(item)
        self.upd_btn.Disable()
        self.del_btn.Disable()

    def on_close(self, e: wx.Event):
        get_app().refresh()
        e.Skip()

    def on_search(self, e: wx.CommandEvent):
        match e.GetString().strip().casefold():
            case "":
                pass
            case s:
                self.listctrl.DeleteAllItems()
                for item in filter(
                    lambda r: s in r["name"].casefold(),
                    get_app().service_store,
                ):
                    self.listctrl.append(item)

    def on_text(self, e: wx.CommandEvent):
        if e.GetString() == "":
            self.refresh()
        else:
            self.upd_btn.Disable()
            self.del_btn.Disable()

    def on_select(self, _):
        self.upd_btn.Enable()
        self.del_btn.Enable()

    def on_deselect(self, _):
        self.upd_btn.Disable()
        self.del_btn.Disable()

    def on_add(self, _):
        AddDialog(self).ShowModal()
        self.refresh()

    def on_upd(self, _):
        item = self.listctrl.GetFirstSelected()
        assert item >= 0
        UpdateDialog(
            self,
            id=int(self.listctrl.GetItemText(item, 0)),
            name=self.listctrl.GetItemText(item, 1),
            price=self.listctrl.GetItemText(item, 2),
        ).ShowModal()
        self.refresh()

    def on_del(self, _):
        item = self.listctrl.GetFirstSelected()
        assert item >= 0
        id = int(self.listctrl.GetItemText(item, 0))
        app = get_app()
        if (
            wx.MessageBox(
                f"{self.listctrl.GetItemText(item, 1)}",
                "Xoá dịch vụ",
                style=wx.YES_NO | wx.NO_DEFAULT,
            )
            == wx.YES
        ):
            try:
                delete(app.conn, ServiceStore, id)
                app.fetch_service_store()
            except sqlite3.Error as error:
                wx.MessageBox(str(error), "Không xoá được")
        self.refresh()
