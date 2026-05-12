import wx
from lib.wx_helper import EA, row
from lib.wx_helper.widget import GenderChoiceCtrl
import wx.adv


class Box(wx.Panel):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        sz = wx.StaticBoxSizer(wx.VERTICAL, self, label="Thông tin bệnh nhân")
        box = sz.GetStaticBox()
        self.name = wx.TextCtrl(box)
        self.gender = GenderChoiceCtrl(box)
        self.birthdate = wx.adv.DatePickerCtrl(box)
        self.age = wx.TextCtrl(box, size=wx.Size(120, -1), style=wx.TE_READONLY)
        self.past_history = wx.TextCtrl(box, style=wx.TE_MULTILINE)

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
            (self.age, 0, EA, 0),
        )
        row2 = row(
            static("Tiền căn: ", 100),
            (self.past_history, 1, EA, 0),
        )

        sz.AddMany(
            [
                (row1, 0, EA, 5),
                (row2, 1, EA, 5),
            ]
        )
        self.SetSizerAndFit(sz)
        self.SetOwnBackgroundColour(wx.Colour(230, 239, 254))
