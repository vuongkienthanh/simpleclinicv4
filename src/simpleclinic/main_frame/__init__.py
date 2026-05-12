import wx
from lib.wx_helper import get_app, row, column, EA
from ._widget import patient_list, visit_list, patient_info, visit_info, visit_book


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(
            parent=None, pos=wx.Point(0, 20), title="PHẦN MỀM PHÒNG KHÁM SIMPLE CLINIC"
        )
        self.SetFont(wx.Font(wx.FontInfo(get_app().config["theme"]["font_size"])))
        self.Maximize()

        self.patient_search = wx.SearchCtrl(self)
        self.patient_list = patient_list.BookCtrl(self)
        self.visit_list = visit_list.ListCtrl(self)
        self.patient_info = patient_info.Box(self)
        self.visit_info = visit_info.Box(self)
        self.visit_book = visit_book.BookCtrl(self)

        left = column(
            (self.patient_search, 0, EA, 5),
            (self.patient_list, 2, EA, 5),
            (self.visit_list, 1, EA, 5),
        )
        right = column(
            (self.patient_info, 1, EA, 5),
            (self.visit_info, 1, EA, 5),
            (self.visit_book, 0, EA, 5),
        )
        self.SetSizerAndFit(
            row(
                (left, 2, EA, 5),
                (right, 3, EA, 5),
            )
        )
