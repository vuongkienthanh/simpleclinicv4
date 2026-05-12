import wx

from . import order_medicine, order_service
from lib.paths import MEDICINE_BM, SERVICE_BM


class Book(wx.Notebook):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self.AddPage(order_medicine.Panel(self), "Đơn thuốc", select=True)
        self.AddPage(order_service.Panel(self), "Dịch vụ")

        images = wx.ImageList(16, 16)
        images.Add(wx.Bitmap(str(MEDICINE_BM)))
        images.Add(wx.Bitmap(str(SERVICE_BM)))
        self.SetImageList(images)
        self.SetPageImage(0, 0)
        self.SetPageImage(1, 1)
