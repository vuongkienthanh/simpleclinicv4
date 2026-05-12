import wx
from lib.enums import Gender


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
