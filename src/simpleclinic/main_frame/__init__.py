from typing import cast
import sqlite3
import wx
import wx.adv
from wx.lib.intctrl import IntCtrl
from wx.lib.masked.numctrl import NumCtrl

from lib.paths import (
    WEIGHT_BM,
    MEDICINE_BM,
    SERVICE_BM,
    PLUS_BM,
    MINUS_BM,
    UPDATE_BM,
    OK_BM,
    CANCEL_BM,
)
from lib.wx_helper import get_app, row, column, EA
from lib.wx_helper.widget import GenderChoiceCtrl, DoseCtrl
from lib.models import Patient
from lib.enums import Gender
from lib.db import insert, update
from lib.vn import bd_to_vn_age
from ._widget import (
    patient,
    visit,
    medicine,
    service,
)


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(
            parent=None, pos=wx.Point(0, 20), title="PHẦN MỀM PHÒNG KHÁM SIMPLE CLINIC"
        )
        self.SetFont(wx.Font(wx.FontInfo(get_app().config["theme"]["font_size"])))
        self.SetBackgroundColour(wx.Colour(get_app().config["theme"]["main_frame"]))
        self.Maximize()

        patient_search = wx.SearchCtrl(self)
        patient_book = wx.Notebook(self)
        queue = patient.List(patient_book)
        seentoday = patient.List(patient_book)
        follow_up = patient.List(patient_book)
        patient_book.AddPage(page=queue, text="Danh sách BN", select=True)
        patient_book.AddPage(page=seentoday, text="Đã khám hôm nay")
        patient_book.AddPage(page=follow_up, text="Tái khám")
        visit_list = visit.List(self)
        patient_info = wx.StaticBoxSizer(wx.VERTICAL, self, label="Thông tin bệnh nhân")
        self.patient_box = patient_info.GetStaticBox()
        self.patient_box.SetOwnBackgroundColour(
            wx.Colour(*get_app().config["theme"]["patient_info"])
        )
        self.patient_name = wx.TextCtrl(self.patient_box)
        self.patient_gender = GenderChoiceCtrl(self.patient_box)
        self.patient_birthdate = wx.adv.DatePickerCtrl(self.patient_box)
        self.patient_birthdate.SetRange(wx.DateTime(), wx.DateTime.Today())
        self.patient_age = wx.TextCtrl(
            self.patient_box, size=wx.Size(120, -1), style=wx.TE_READONLY
        )
        self.patient_age.Disable()
        self.patient_age.ChangeValue(bd_to_vn_age(wx.DateTime.Today()))
        self.patient_past_history = wx.TextCtrl(
            self.patient_box, style=wx.TE_MULTILINE, size=wx.Size(-1, 75)
        )
        self.patient_new_btn = wx.Button(self.patient_box, label="BN Mới")
        self.patient_upd_btn = wx.Button(self.patient_box, label="Cập nhật")
        self.patient_ok_btn = wx.Button(self.patient_box, label="OK")
        self.patient_cancel_btn = wx.Button(self.patient_box, label="Cancel")
        visit_info = wx.StaticBoxSizer(wx.VERTICAL, self, label="Thông tin lượt khám")
        self.visit_box = visit_info.GetStaticBox()
        self.visit_box.SetOwnBackgroundColour(
            wx.Colour(*get_app().config["theme"]["visit_info"])
        )
        self.visit_weight = NumCtrl(
            self.visit_box, fractionWidth=1, min=0, limited=True
        )
        get_weight = wx.BitmapButton(
            self.visit_box, bitmap=wx.BitmapBundle(wx.Bitmap(str(WEIGHT_BM)))
        )
        get_weight.SetToolTip("Lấy cân nặng mới nhất")
        self.visit_days = IntCtrl(
            self.visit_box,
            value=get_app().config["process"]["default_days_for_prescription"],
            min=0,
            limited=True,
        )
        self.visit_price = IntCtrl(self.visit_box, min=0, limited=True)
        self.visit_price_txt = wx.StaticText(
            self.visit_box, label="", size=wx.Size(100, -1)
        )
        self.visit_medical_history = wx.TextCtrl(self.visit_box, style=wx.TE_MULTILINE)
        self.visit_diagnosis = wx.TextCtrl(self.visit_box)
        self.visit_note = wx.TextCtrl(self.visit_box)

        order_info = wx.Notebook(self)
        order_info.SetBackgroundColour(
            wx.Colour(*get_app().config["theme"]["order_info"])
        )

        medicine_page = wx.Panel(order_info)
        self.medicine_search = medicine.Picker(medicine_page)
        self.medicine_times = IntCtrl(medicine_page, min=0, limited=True)
        self.medicine_dose = DoseCtrl(medicine_page)
        self.medicine_usage_unit = wx.StaticText(medicine_page, label="{đơn vị}")
        self.medicine_quantity = IntCtrl(medicine_page, min=0, limited=True)
        self.medicine_selling_unit = wx.StaticText(medicine_page, label="{đơn vị}")
        self.medicine_usage_note = wx.TextCtrl(medicine_page)
        self.medicine_price_txt = wx.StaticText(
            medicine_page, label="Đơn giá: ", size=wx.Size(150, -1)
        )
        medicine_buttons = wx.Panel(medicine_page, size=wx.Size(120, -1))
        self.medicine_add_btn = wx.BitmapButton(
            medicine_buttons, bitmap=wx.BitmapBundle(wx.Bitmap(str(PLUS_BM)))
        )
        self.medicine_upd_btn = wx.BitmapButton(
            medicine_buttons, bitmap=wx.BitmapBundle(wx.Bitmap(str(UPDATE_BM)))
        )
        self.medicine_del_btn = wx.BitmapButton(
            medicine_buttons, bitmap=wx.BitmapBundle(wx.Bitmap(str(MINUS_BM)))
        )
        self.medicine_ok_btn = wx.BitmapButton(
            medicine_buttons, bitmap=wx.BitmapBundle(wx.Bitmap(str(OK_BM)))
        )
        self.medicine_cancel_btn = wx.BitmapButton(
            medicine_buttons, bitmap=wx.BitmapBundle(wx.Bitmap(str(CANCEL_BM)))
        )
        self.medicine_list = medicine.List(medicine_page)

        service_page = wx.Panel(order_info)
        self.service_search = service.Picker(service_page)
        self.service_quantity = IntCtrl(service_page, min=0, limited=True)
        self.service_price_txt = wx.StaticText(
            service_page, label="Đơn giá: ", size=wx.Size(150, -1)
        )
        service_buttons = wx.Panel(service_page, size=wx.Size(120, -1))
        self.service_add_btn = wx.BitmapButton(
            service_buttons, bitmap=wx.BitmapBundle(wx.Bitmap(str(PLUS_BM)))
        )
        self.service_upd_btn = wx.BitmapButton(
            service_buttons, bitmap=wx.BitmapBundle(wx.Bitmap(str(UPDATE_BM)))
        )
        self.service_del_btn = wx.BitmapButton(
            service_buttons, bitmap=wx.BitmapBundle(wx.Bitmap(str(MINUS_BM)))
        )
        self.service_ok_btn = wx.BitmapButton(
            service_buttons, bitmap=wx.BitmapBundle(wx.Bitmap(str(OK_BM)))
        )
        self.service_cancel_btn = wx.BitmapButton(
            service_buttons, bitmap=wx.BitmapBundle(wx.Bitmap(str(CANCEL_BM)))
        )
        self.service_list = service.List(service_page)

        order_info.AddPage(medicine_page, "Đơn thuốc", select=True)
        order_info.AddPage(service_page, "Dịch vụ")

        images = wx.ImageList(16, 16)
        images.Add(wx.Bitmap(str(MEDICINE_BM)))
        images.Add(wx.Bitmap(str(SERVICE_BM)))
        order_info.SetImageList(images)
        order_info.SetPageImage(0, 0)
        order_info.SetPageImage(1, 1)

        self.visit_new_btn = wx.Button(self, label="Lượt khám mới")
        self.visit_same_btn = wx.Button(self, label="Lượt khám mới (toa cũ)")
        self.visit_upd_btn = wx.Button(self, label="Cập nhật")
        self.visit_ok_btn = wx.Button(self, label="OK")
        self.visit_cancel_btn = wx.Button(self, label="Cancel")

        def static(parent, label: str, w=-1):
            return (
                wx.StaticText(parent, label=label, size=wx.Size(w, -1)),
                0,
                wx.ALIGN_CENTER_VERTICAL,
                0,
            )

        row1 = row(
            static(self.patient_box, "Họ tên: ", 100),
            (self.patient_name, 1, EA, 2),
            static(self.patient_box, "Giới: "),
            (self.patient_gender, 0, EA, 2),
            static(self.patient_box, "SN: "),
            (self.patient_birthdate, 0, EA, 2),
            static(self.patient_box, "Tuổi: "),
            (self.patient_age, 0, EA, 2),
        )
        row2 = row(
            static(self.patient_box, "Tiền căn: ", 100),
            (self.patient_past_history, 1, EA, 2),
        )
        row3 = row(
            (self.patient_new_btn, 0, EA, 5),
            (self.patient_upd_btn, 0, EA, 5),
            (self.patient_ok_btn, 0, EA, 5),
            (self.patient_cancel_btn, 0, EA, 5),
        )

        patient_info.AddMany(
            [
                (row1, 0, EA, 5),
                (row2, 1, EA, 5),
                (row3, 0, EA, 5),
            ]
        )
        row1 = row(
            static(self.visit_box, "Cân nặng: ", 100),
            (self.visit_weight, 0, EA, 2),
            (get_weight, 0, EA, 2),
            static(self.visit_box, "Số ngày thuốc: "),
            (self.visit_days, 0, EA, 2),
            (0, 0, 3),
            static(self.visit_box, "Giá tiền: "),
            (self.visit_price, 0, EA, 2),
            (self.visit_price_txt, 0, wx.ALIGN_CENTER_VERTICAL, 2),
        )
        row2 = row(
            static(self.visit_box, "Bệnh sử: ", 100),
            (self.visit_medical_history, 1, EA, 2),
        )
        row3 = row(
            static(self.visit_box, "Chẩn đoán: ", 100),
            (self.visit_diagnosis, 1, EA, 2),
        )
        row4 = row(
            static(self.visit_box, "Ghi chú: ", 100),
            (self.visit_note, 1, EA, 2),
        )
        visit_info.AddMany(
            [
                (row1, 0, EA, 5),
                (row2, 1, EA, 5),
                (row3, 0, EA, 5),
                (row4, 0, EA, 5),
            ]
        )

        medicine_buttons.SetSizer(
            row(
                (self.medicine_add_btn, 0, EA, 2),
                (self.medicine_upd_btn, 0, EA, 2),
                (self.medicine_del_btn, 0, EA, 2),
                (self.medicine_ok_btn, 0, EA, 2),
                (self.medicine_cancel_btn, 0, EA, 2),
            )
        )

        row1 = row(
            static(medicine_page, "Thuốc: ", 100),
            (self.medicine_search, 1, EA, 2),
            static(medicine_page, "Ngày "),
            (self.medicine_times, 0, EA, 2),
            static(medicine_page, "lần, lần"),
            (self.medicine_dose, 0, EA, 2),
            (self.medicine_usage_unit, 0, wx.ALIGN_CENTER_VERTICAL, 2),
            static(medicine_page, "Tổng: "),
            (self.medicine_quantity, 0, EA, 2),
            (self.medicine_selling_unit, 0, wx.ALIGN_CENTER_VERTICAL, 2),
            (medicine_buttons, 0, EA, 2),
        )
        row2 = row(
            static(medicine_page, "Cách sử dụng:", 120),
            (self.medicine_usage_note, 1, EA, 2),
            (self.medicine_price_txt, 0, wx.ALIGN_CENTER_VERTICAL, 2),
        )
        medicine_page.SetSizer(
            column((row1, 0, EA, 5), (row2, 0, EA, 5), (self.medicine_list, 1, EA, 5))
        )

        service_buttons.SetSizer(
            row(
                (self.service_add_btn, 0, EA, 2),
                (self.service_upd_btn, 0, EA, 2),
                (self.service_del_btn, 0, EA, 2),
                (self.service_ok_btn, 0, EA, 2),
                (self.service_cancel_btn, 0, EA, 2),
            )
        )

        row1 = row(
            static(service_page, "Dịch vụ: ", 100),
            (self.service_search, 1, EA, 2),
            static(service_page, "Tổng: "),
            (self.service_quantity, 0, EA, 2),
            (self.service_price_txt, 0, wx.ALIGN_CENTER_VERTICAL, 2),
            (service_buttons, 0, EA, 2),
        )
        service_page.SetSizer(column((row1, 0, EA, 5), (self.service_list, 1, EA, 5)))

        left = column(
            (patient_search, 0, EA, 5),
            (patient_book, 2, EA, 5),
            (visit_list, 1, EA, 5),
        )
        right = column(
            (patient_info, 0, EA, 5),
            (visit_info, 0, EA, 5),
            (order_info, 1, EA, 5),
            row(
                (self.visit_new_btn, 0, EA, 5),
                (self.visit_same_btn, 0, EA, 5),
                (self.visit_upd_btn, 0, EA, 5),
                (self.visit_ok_btn, 0, EA, 5),
                (self.visit_cancel_btn, 0, EA, 5),
            ),
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

        patient_book.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_patient_select)
        patient_book.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_patient_deselect)
        visit_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_visit_select)
        visit_list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_visit_deselect)
        self.patient_birthdate.Bind(wx.adv.EVT_DATE_CHANGED, self.on_date_changed)
        self.patient_new_btn.Bind(wx.EVT_BUTTON, self.on_patient_new_btn)
        self.patient_upd_btn.Bind(wx.EVT_BUTTON, self.on_patient_upd_btn)
        self.patient_ok_btn.Bind(wx.EVT_BUTTON, self.on_patient_ok_btn)
        self.patient_cancel_btn.Bind(wx.EVT_BUTTON, self.on_patient_cancel_btn)
        get_weight.Bind(wx.EVT_BUTTON, self.on_get_weight)
        self.visit_price.Bind(wx.EVT_TEXT, self.on_price_changed)
        self.patient_edit_mode(False)
        self.visit_edit_mode(False)
        self.medicine_edit_mode(False)
        self.service_edit_mode(False)
        patient_search.SetFocus()

    @property
    def patient_id(self) -> int | None:
        self._patient_id

    @patient_id.setter
    def patient_id(self, value: int | None):
        if value is None:
            self._patient_id = value
            self.patient_box.SetLabel("Thông tin bệnh nhân:")
            self.patient_name.Clear()
            self.patient_gender.SetGender(Gender(0))
            self.patient_birthdate.SetValue(wx.DateTime.Today())
            self.patient_past_history.Clear()
            self.patient_upd_btn.Disable()
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
                self.patient_box.SetLabel(f"Thông tin bệnh nhân: {value}")
                self.patient_name.SetValue(patient["name"])
                self.patient_gender.SetGender(patient["gender"])
                self.patient_birthdate.SetValue(patient["birthdate"])
                self.patient_past_history.SetValue(patient["past_history"])
                self.patient_upd_btn.Enable()
            except sqlite3.Error as error:
                wx.MessageBox("Lỗi", str(error))

    @property
    def visit_id(self) -> int | None:
        self._visit_id

    @visit_id.setter
    def visit_id(self, value: int | None):
        if value is None:
            self._visit_id = None
            self.visit_box.SetLabel("Thông tin lượt khám")
            self.visit_weight.SetValue(0)
            # TODO
            self.visit_diagnosis.Clear()
        else:
            ...

    @property
    def medicine_id(self) -> int | None:
        self._medicine_id

    @medicine_id.setter
    def medicine_id(self, value: int | None):
        # TODO
        ...

    @property
    def service_id(self) -> int | None:
        self._medicine_id

    @service_id.setter
    def service_id(self, value: int | None):
        # TODO
        ...

    def on_patient_select(self, e: wx.ListEvent):
        self.patient_id = int(cast(wx.ListCtrl, e.EventObject).GetItemText(e.Index, 0))

    def on_patient_deselect(self, _: wx.ListEvent):
        self.patient_id = None

    def on_visit_select(self, e: wx.ListEvent):
        self.visit_id = int(cast(wx.ListCtrl, e.EventObject).GetItemText(e.Index, 0))

    def on_visit_deselect(self, _: wx.ListEvent):
        self.visit_id = None

    def on_medicine_select(self, e: wx.ListEvent):
        self.medicine_id = int(cast(wx.ListCtrl, e.EventObject).GetItemText(e.Index, 1))

    def on_medicine_deselect(self, _: wx.ListEvent):
        self.medicine_id = None

    def on_service_select(self, e: wx.ListEvent):
        self.service_id = int(cast(wx.ListCtrl, e.EventObject).GetItemText(e.Index, 1))

    def on_service_deselect(self, _: wx.ListEvent):
        self.service_id = None

    def patient_edit_mode(self, b: bool = True):
        self.patient_name.Enable(b)
        self.patient_gender.Enable(b)
        self.patient_birthdate.Enable(b)
        self.patient_past_history.Enable(b)
        self.patient_new_btn.Show(not b)
        self.patient_upd_btn.Show(not b)
        self.patient_ok_btn.Show(b)
        self.patient_cancel_btn.Show(b)

    def visit_edit_mode(self, b: bool = True):
        self.visit_weight.Enable(b)
        self.visit_days.Enable(b)
        self.visit_price.Enable(b)
        self.visit_medical_history.Enable(b)
        self.visit_diagnosis.Enable(b)
        self.visit_note.Enable(b)
        self.visit_new_btn.Show(not b)
        self.visit_same_btn.Show(not b)
        self.visit_upd_btn.Show(not b)
        self.visit_ok_btn.Show(b)
        self.visit_cancel_btn.Show(b)

    def medicine_edit_mode(self, b: bool = True):
        self.medicine_search.Enable(b)
        self.medicine_times.Enable(b)
        self.medicine_dose.Enable(b)
        self.medicine_quantity.Enable(b)
        self.medicine_usage_note.Enable(b)
        self.medicine_add_btn.Show(not b)
        self.medicine_upd_btn.Show(not b)
        self.medicine_del_btn.Show(not b)
        self.medicine_ok_btn.Show(b)
        self.medicine_cancel_btn.Show(b)

    def service_edit_mode(self, b: bool = True):
        self.service_search.Enable(b)
        self.service_quantity.Enable(b)
        self.service_add_btn.Show(not b)
        self.service_upd_btn.Show(not b)
        self.service_del_btn.Show(not b)
        self.service_ok_btn.Show(b)
        self.service_cancel_btn.Show(b)

    def refresh(self): ...

    def on_date_changed(self, e: wx.adv.DateEvent):
        self.patient_age.ChangeValue(bd_to_vn_age(e.GetDate()))

    def on_patient_new_btn(self, _):
        self.patient_id = None
        self.patient_edit_mode()

    def on_patient_upd_btn(self, _):
        self.patient_edit_mode()

    def on_patient_ok_btn(self, _):
        id = self.patient_id
        patient = Patient(
            name=self.patient_name.Value.strip().upper(),
            gender=self.patient_gender.GetGender(),
            birthdate=self.patient_birthdate.Value,
            past_history=self.patient_past_history.Value.strip(),
        )
        try:
            if id is None:
                id = insert(get_app().conn, patient)
                self._patient_id = id
            else:
                update(get_app().conn, patient, id)
        except sqlite3.Error as error:
            wx.MessageBox("Lỗi", str(error))

        self.patient_edit_mode(False)

    def on_patient_cancel_btn(self, _):
        id = self.patient_id
        if id is None:
            self.patient_id = None
        else:
            self.patient_id = id

        self.patient_edit_mode(False)

    def on_get_weight(self, _):
        id = self.patient_id
        if id is not None:
            try:
                last_weight = (
                    get_app()
                    .conn.execute(
                        """
                    SELECT weight FROM visits WHERE patient_id = ?
                    ORDER BY exam_datetime DESC
                    LIMIT 1
                        """,
                        (id,),
                    )
                    .fetchone()
                )
                self.visit_weight.SetValue(last_weight / 10)
            except sqlite3.Error as error:
                wx.MessageBox("Lỗi", str(error))

    def on_price_changed(self, e):
        self.visit_price_txt.SetLabel(f"{int(e.String):,}")
