import wx
from . import medicine_info
from lib.paths import MEDICINE_BM


class BookCtrl(wx.Notebook):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        tab1 = medicine_info.Panel(self)
        self.AddPage(tab1, "Đơn thuốc", select=True)

        images = wx.ImageList(16, 16)
        images.Add(wx.Bitmap(str(MEDICINE_BM)))
        self.SetImageList(images)
        self.SetPageImage(0, 0)
