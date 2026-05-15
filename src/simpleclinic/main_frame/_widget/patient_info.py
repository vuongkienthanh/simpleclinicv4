import wx
from lib.models import Patient
from lib.wx_helper import EA, get_app, get_main_frame, row
from lib.wx_helper.widget import GenderChoiceCtrl
import wx.adv
from lib.vn import bd_to_vn_age
from lib.db import insert, update
import sqlite3


class Box(wx.Panel):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self.SetOwnBackgroundColour(
            wx.Colour(*get_app().config["theme"]["patient_info"])
        )
        sz = wx.StaticBoxSizer(wx.VERTICAL, self, label="Thông tin bệnh nhân")
        box = sz.GetStaticBox()
        self.name = wx.TextCtrl(box)
        self.gender = GenderChoiceCtrl(box)
        self.birthdate = wx.adv.DatePickerCtrl(box)
        self.age = wx.TextCtrl(box, size=wx.Size(120, -1), style=wx.TE_READONLY)
        self.age.Disable()
        self.past_history = wx.TextCtrl(
            box, style=wx.TE_MULTILINE, size=wx.Size(-1, 75)
        )
        self.new_btn = wx.Button(box, label="BN Mới")
        self.upd_btn = wx.Button(box, label="Cập nhật")
        self.ok_btn = wx.Button(box, label="OK")
        self.cancel_btn = wx.Button(box, label="Cancel")

        def static(label: str, w=-1):
            return (
                wx.StaticText(box, label=label, size=wx.Size(w, -1)),
                0,
                wx.ALIGN_CENTER_VERTICAL,
                0,
            )

        row1 = row(
            static("Họ tên: ", 100),
            (self.name, 1, EA, 2),
            static("Giới: "),
            (self.gender, 0, EA, 2),
            static("SN: "),
            (self.birthdate, 0, EA, 2),
            static("Tuổi: "),
            (self.age, 0, EA, 2),
        )
        row2 = row(
            static("Tiền căn: ", 100),
            (self.past_history, 1, EA, 2),
        )
        row3 = row(
            (self.new_btn, 0, EA, 5),
            (self.upd_btn, 0, EA, 5),
            (self.ok_btn, 0, EA, 5),
            (self.cancel_btn, 0, EA, 5),
        )

        sz.AddMany(
            [
                (row1, 0, EA, 5),
                (row2, 1, EA, 5),
                (row3, 0, EA, 5),
            ]
        )
        self.SetSizerAndFit(sz)

        self.name.Disable()
        self.gender.Disable()
        self.birthdate.Disable()
        self.past_history.Disable()
        self.upd_btn.Disable()
        self.ok_btn.Hide()
        self.cancel_btn.Hide()

        self.birthdate.Bind(wx.adv.EVT_DATE_CHANGED, self.on_date_changed)
        self.new_btn.Bind(wx.EVT_BUTTON, self.on_new)
        self.upd_btn.Bind(wx.EVT_BUTTON, self.on_upd)
        self.ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_date_changed(self, e: wx.adv.DateEvent):
        self.age.ChangeValue(bd_to_vn_age(e.GetDate()))

    def on_new(self, _):
        get_main_frame().patient_id = None
        self.name.Enable()
        self.gender.Enable()
        self.birthdate.Enable()
        self.past_history.Enable()
        self.new_btn.Hide()
        self.upd_btn.Hide()
        self.ok_btn.Show()
        self.cancel_btn.Show()

    def on_upd(self, _):
        self.name.Enable()
        self.gender.Enable()
        self.birthdate.Enable()
        self.past_history.Enable()
        self.new_btn.Hide()
        self.upd_btn.Hide()
        self.ok_btn.Show()
        self.cancel_btn.Show()

    def on_ok(self, _):
        id = get_main_frame().patient_id
        patient = Patient(
            name=self.name.Value.strip().upper(),
            gender=self.gender.GetGender(),
            birthdate=self.birthdate.Value,
            past_history=self.past_history.Value,
        )
        try:
            if id is None:
                id = insert(get_app().conn, patient)
                get_main_frame()._patient_id = id  # pyright: ignore[reportPrivateUsage]
            else:
                update(get_app().conn, patient, id)
        except sqlite3.Error as error:
            wx.MessageBox("Lỗi", str(error))

        self.name.Disable()
        self.gender.Disable()
        self.birthdate.Disable()
        self.past_history.Disable()
        self.new_btn.Show()
        self.upd_btn.Show()
        self.ok_btn.Hide()
        self.cancel_btn.Hide()

    def on_cancel(self, _):
        id = get_main_frame().patient_id
        if id is None:
            get_main_frame().patient_id = None
        else:
            get_main_frame().patient_id = id

        self.name.Disable()
        self.gender.Disable()
        self.birthdate.Disable()
        self.past_history.Disable()
        self.new_btn.Show()
        self.upd_btn.Show()
        self.ok_btn.Hide()
        self.cancel_btn.Hide()
