import wx
import wx.adv
from lib.wx_helper import EA, row, column
from lib.wx_helper.widget import GenderChoiceCtrl
from lib.enums import Gender
from lib.vn import bd_to_vn_age
from lib.models import Patient


class Dialog(wx.Dialog):
    def __init__(
        self,
        parent: wx.Window,
        title: str,
        id: int | None = None,
        name: str = "",
        gender: Gender = Gender.m,
        birthdate: wx.DateTime = wx.InvalidDateTime,
        past_history: str = "",
    ):
        if not birthdate.IsValid():
            birthdate = wx.DateTime.Today()
        super().__init__(
            parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )

        self.name = wx.TextCtrl(self, name="Họ tên")
        self.gender = GenderChoiceCtrl(self, name="Giới tính")
        self.birthdate = wx.adv.DatePickerCtrl(self, name="Ngày sinh")
        self.age = wx.StaticText(self, label="", name="Tuổi")
        self.past_history = wx.TextCtrl(
            self, style=wx.TE_MULTILINE, name="Bệnh nền, dị ứng"
        )
        self.okbtn = wx.Button(self, label="OK")
        self.cancelbtn = wx.Button(self, label="Cancel")

        self.id = id
        self.name.ChangeValue(name)
        self.gender.SetGender(gender)
        self.birthdate.SetValue(birthdate)
        self.age.SetLabel(bd_to_vn_age(birthdate))
        self.past_history.ChangeValue(past_history)

        def widget(w: wx.Window):
            left = EA | wx.ALIGN_CENTER_VERTICAL
            right = EA
            return (wx.StaticText(self, label=w.Name), 0, left, 3), (w, 1, right, 3)

        info_sizer = wx.FlexGridSizer(5, 2, 3, 3)
        info_sizer.AddGrowableCol(1, 1)
        info_sizer.AddGrowableRow(4, 1)
        info_sizer.AddMany(
            [
                *widget(self.name),
                *widget(self.gender),
                *widget(self.birthdate),
                *widget(self.age),
                *widget(self.past_history),
            ]
        )
        btn_sizer = row(
            (0, 0, 1),
            (self.okbtn, 0, wx.RIGHT, 5),
            (self.cancelbtn, 0, wx.RIGHT, 5),
        )

        self.SetSizerAndFit(
            column((info_sizer, 1, wx.EXPAND, 0), (btn_sizer, 0, wx.EXPAND | wx.ALL, 5))
        )

        self.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.on_birthdate)
        self.Bind(wx.EVT_BUTTON, self.on_ok, source=self.okbtn)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, source=self.cancelbtn)

    def on_birthdate(self, e: wx.adv.CalendarEvent):
        date = e.GetDate()
        self.age.SetLabel(bd_to_vn_age(date))

    def on_ok(self, _): ...

    def on_cancel(self, _):
        self.Close()

    def get_item(self):
        return Patient(
            name=self.name.Value.strip(),
            gender=self.gender.GetGender(),
            birthdate=self.birthdate.GetValue(),
            past_history=self.past_history.GetValue().strip(),
        )
