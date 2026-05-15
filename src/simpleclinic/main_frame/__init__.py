import sqlite3
import wx
from lib.wx_helper import get_app, row, column, EA
from ._widget import patient_book, visit_list, patient_info, visit_info, order_info
from . import _buttons
from lib.enums import Gender


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(
            parent=None, pos=wx.Point(0, 20), title="PHẦN MỀM PHÒNG KHÁM SIMPLE CLINIC"
        )
        self.SetFont(wx.Font(wx.FontInfo(get_app().config["theme"]["font_size"])))
        self.SetBackgroundColour(wx.Colour(get_app().config["theme"]["main_frame"]))
        self.Maximize()

        self.patient_search = wx.SearchCtrl(self)
        self.patient_list = patient_book.Book(self)
        self.visit_list = visit_list.List(self)
        self.patient_info = patient_info.Box(self)
        self.visit_info = visit_info.Box(self)
        self.visit_book = order_info.Book(self)

        left = column(
            (self.patient_search, 0, EA, 5),
            (self.patient_list, 2, EA, 5),
            (self.visit_list, 1, EA, 5),
        )
        right = column(
            (self.patient_info, 0, EA, 5),
            (self.visit_info, 0, EA, 5),
            (self.visit_book, 1, EA, 5),
            (_buttons.Panel(self), 0, EA, 5),
        )
        self.SetSizerAndFit(
            row(
                (left, 2, EA, 5),
                (right, 3, EA, 5),
            )
        )

        # DATA
        self._patient_id: int | None
        self._visit_id: int | None
        self._medicine_id: int | None
        self._service_id: int | None

        self.patient_id = None
        self.visit_id = None
        self.medicine_id = None
        self.service_id = None

    @property
    def patient_id(self) -> int | None:
        self._patient_id

    @patient_id.setter
    def patient_id(self, value: int | None):
        if value is None:
            self._patient_id = value
            self.patient_info.GetSizer().GetStaticBox().SetLabel("Thông tin bệnh nhân:")  # pyright: ignore[reportAttributeAccessIssue]
            self.patient_info.name.Clear()
            self.patient_info.gender.SetGender(Gender(0))
            self.patient_info.birthdate.SetValue(wx.DateTime.Today())
            self.patient_info.past_history.Clear()
        else:
            try:
                self._patient_id = value
                patient = (
                    get_app()
                    .conn.execute(
                        "SELECT name, gender, birthdate, past_history FROM patients where id = ?",
                        (value,),
                    )
                    .fetchone()
                )
                self.patient_info.GetSizer().GetStaticBox().SetLabel(  # pyright: ignore[reportAttributeAccessIssue]
                    f"Thông tin bệnh nhân: {value}"
                )
                self.patient_info.name.SetValue(patient["name"])
                self.patient_info.gender.SetGender(patient["gender"])
                self.patient_info.birthdate.SetValue(patient["birthdate"])
                self.patient_info.past_history.SetValue(patient["past_history"])
            except sqlite3.Error as error:
                wx.MessageBox("Lỗi", str(error))

    @property
    def visit_id(self) -> int | None:
        self._visit_id

    @visit_id.setter
    def visit_id(self, value: int | None):
        if value is None:
            self._visit_id = None
            self.visit_info.GetSizer().GetStaticBox().SetLabel("Thông tin lượt khám")  # pyright: ignore[reportAttributeAccessIssue]
            self.visit_info.weight.SetValue(0)
            # TODO
            self.visit_info.diagnosis.Clear()
        else:
            ...
