import wx
from lib.enums import Gender
from lib.wx_helper import (
    NUMBERS,
    NUMPADS,
    SPECIALS,
    SLASH,
    DECIMAL,
)


class GenderChoiceCtrl(wx.Choice):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent, choices=[Gender(0).display_name, Gender(1).display_name], **kwargs
        )
        self.Selection = 0

    def GetGender(self) -> Gender:
        return Gender(self.Selection)

    def SetGender(self, gender: Gender):
        self.SetSelection(gender.value)


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
