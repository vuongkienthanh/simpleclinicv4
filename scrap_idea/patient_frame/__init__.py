import sqlite3
import wx
from ._widget import ListCtrl
from simpleclinic.patient_dialog import AddDialog, UpdateDialog
from lib.wx_helper import row, column, get_app, EA
from lib.db import delete,  DATE_FORMAT
from lib.enums import Gender
from lib.models import Patient


class PatientFrame(wx.Frame):
    def __init__(self):

        super().__init__(parent=None, title="Danh sách bệnh nhân")
        self.searchctrl = wx.SearchCtrl(self)
        self.listctrl = ListCtrl(self)
        self.addbtn = wx.Button(self, label="Thêm mới")
        self.updbtn = wx.Button(self, label="Cập nhật")
        self.delbtn = wx.Button(self, label="Xoá")

        search_sizer = row(
            (wx.StaticText(self, label="Tìm kiếm"), 0, wx.ALL | wx.ALIGN_CENTER, 5),
            (self.searchctrl, 1, wx.ALL, 5),
        )
        btn_sizer = row(
            (0, 0, 1),
            (self.addbtn, 0, wx.RIGHT, 5),
            (self.updbtn, 0, wx.RIGHT, 5),
            (self.delbtn, 0, wx.RIGHT, 5),
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
        self.Bind(wx.EVT_BUTTON, self.on_add, source=self.addbtn)
        self.Bind(wx.EVT_BUTTON, self.on_upd, source=self.updbtn)
        self.Bind(wx.EVT_BUTTON, self.on_del, source=self.delbtn)

    def refresh(self):
        self.searchctrl.ChangeValue("")
        self.listctrl.DeleteAllItems()
        self.updbtn.Disable()
        self.delbtn.Disable()

    def on_close(self, e: wx.Event):
        get_app().refresh()
        e.Skip()

    def on_search(self, e: wx.CommandEvent):
        match e.GetString().strip():
            case "":
                pass
            case s:
                self.listctrl.DeleteAllItems()
                for item in (
                    get_app()
                    .conn.execute(
                        """
                        SELECT id, name, gender, birthdate from patients
                        WHERE name LIKE ?
                        """,
                        (f"%{s}%",),
                    )
                    .fetchall()
                ):
                    self.listctrl.append(item)

    def on_text(self, e: wx.CommandEvent):
        if e.GetString() == "":
            self.refresh()
        else:
            self.updbtn.Disable()
            self.delbtn.Disable()

    def on_select(self, _):
        self.updbtn.Enable()
        self.delbtn.Enable()

    def on_deselect(self, _):
        self.updbtn.Disable()
        self.delbtn.Disable()


    def on_add(self, _):
        AddDialog(self).ShowModal()
        self.refresh()

    def on_upd(self, _):
        item = self.listctrl.GetFirstSelected()
        assert item >= 0
        UpdateDialog(
            self,
            id=int(self.listctrl.GetItemText(item, 0)),
            name=Gender(self.listctrl.GetItemText(item, 1)),
            gender=self.listctrl.GetItemText(item, 2),
            birthdate=wx.DateTime().ParseFormat(
                self.listctrl.GetItemText(item, 3), format=DATE_FORMAT
            ),
            past_history=self.listctrl.GetItemText(item, 4),
        ).ShowModal()
        self.refresh()

    def on_del(self, _):
        item = self.listctrl.GetFirstSelected()
        assert item >= 0
        id = int(self.listctrl.GetItemText(item, 0))
        app = get_app()
        if (
            wx.MessageBox(
                "Xoá bệnh nhân",
                f"{self.listctrl.GetItemText(item, 1)}",
                style=wx.YES_NO | wx.NO_DEFAULT,
            )
            == wx.YES
        ):
            try:
                delete(app.conn, Patient, id)
            except sqlite3.Error as error:
                wx.MessageBox("Không xoá được", f"{error}")
        self.refresh()
