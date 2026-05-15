import wx
from lib.wx_helper import row, EA


class Panel(wx.Panel):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self.new_btn = wx.Button(self, label="Lượt khám mới")
        self.same_btn = wx.Button(self, label="Lượt khám mới (toa cũ)")
        self.upd_btn = wx.Button(self, label="Cập nhật")
        self.ok_btn = wx.Button(self, label="OK")
        self.cancel_btn = wx.Button(self, label="Cancel")

        self.SetSizerAndFit(
            row(
                (self.new_btn, 0, EA, 5),
                (self.same_btn, 0, EA, 5),
                (self.upd_btn, 0, EA, 5),
                (self.ok_btn, 0, EA, 5),
                (self.cancel_btn, 0, EA, 5),
            )
        )
