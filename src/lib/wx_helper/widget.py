import wx
from itertools import chain
from lib.enums import Gender
from . import (
    NUMBERS,
    NUMPADS,
    SPECIALS,
    SLASH,
    DECIMAL,
)
from decimal import Decimal

INT_KEYS = NUMBERS + NUMPADS + SPECIALS


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
        s = self.Value
        if "/" not in s and "." not in s:
            keys = chain(INT_KEYS, SLASH, DECIMAL)
        else:
            keys = INT_KEYS

        if e.KeyCode in keys:
            e.Skip()


class DecimalIntCtrl(wx.TextCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self.Bind(wx.EVT_CHAR, self.on_char)

    def on_char(self, e: wx.KeyEvent):
        s = self.Value
        if "." in s:
            keys = INT_KEYS
        else:
            keys = chain(INT_KEYS, DECIMAL)

        if e.KeyCode in keys:
            e.Skip()

    def GetInt(self) -> Decimal:
        return Decimal(self.Value)

    def SetInt(self, value: Decimal):
        self.ChangeValue(str(value))


class ThousandGroupIntCtrl(wx.TextCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self.Bind(wx.EVT_CHAR, self.on_char)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_TEXT, self.on_text)

    def on_char(self, e: wx.KeyEvent):
        if e.KeyCode in INT_KEYS:
            e.Skip()

    def on_left_down(self, _):
        self.SetFocus()
        self.SetInsertionPointEnd()

    def on_text(self, _):
        if self.Value != "":
            self.ChangeValue("{:,}".format(int(self.Value.replace(",", ""))))
            self.SetInsertionPointEnd()

    def GetInt(self) -> int:
        return int(self.Value.replace(",", ""))

    def SetInt(self, value: int):
        self.ChangeValue(f"{value:,}")
