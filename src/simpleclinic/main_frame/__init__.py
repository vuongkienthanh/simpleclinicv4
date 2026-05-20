from decimal import Decimal
from math import ceil
from fractions import Fraction
import sqlite3
import wx
import wx.adv
from wx.lib.intctrl import IntCtrl

from lib.paths import (
    MEDICINE_BM,
    SERVICE_BM,
    PLUS_BM,
    MINUS_BM,
)
from lib.wx_helper import get_app, row, column, EA
from lib.wx_helper.widget import (
    GenderChoiceCtrl,
    DoseCtrl,
    ThousandGroupIntCtrl,
    DecimalIntCtrl,
)
from lib.models import Patient, Visit
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

        self.patient_search = wx.SearchCtrl(self)
        self.patient_search.SetHint("Ctrl + o")
        patient_book = wx.Notebook(self)
        self.queue = patient.List(patient_book)
        self.seentoday = patient.List(patient_book)
        self.follow_up = patient.List(patient_book)
        patient_book.AddPage(page=self.queue, text="Danh sách BN", select=True)
        patient_book.AddPage(page=self.seentoday, text="Đã khám hôm nay")
        patient_book.AddPage(page=self.follow_up, text="Tái khám")
        self.visit_list = visit.List(self)
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
        self.patient_new_btn = wx.Button(self.patient_box, label="BN Mới (CTRL + N)")
        self.patient_upd_btn = wx.Button(self.patient_box, label="Cập nhật")
        self.patient_ok_btn = wx.Button(self.patient_box, label="OK")
        self.patient_cancel_btn = wx.Button(self.patient_box, label="Cancel")
        visit_info = wx.StaticBoxSizer(wx.VERTICAL, self, label="Thông tin lượt khám")
        self.visit_box = visit_info.GetStaticBox()
        self.visit_box.SetOwnBackgroundColour(
            wx.Colour(*get_app().config["theme"]["visit_info"])
        )
        self.visit_weight = DecimalIntCtrl(self.visit_box)
        self.visit_days = IntCtrl(self.visit_box, min=0, limited=True)
        self.visit_price = ThousandGroupIntCtrl(self.visit_box)
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
        self.medicine_usage_note = wx.TextCtrl(medicine_page, size=wx.Size(250, -1))
        self.medicine_usage_note_txt = wx.StaticText(
            medicine_page, label="", size=wx.Size(500, -1)
        )
        self.medicine_add_btn = wx.BitmapButton(
            medicine_page, bitmap=wx.BitmapBundle(wx.Bitmap(str(PLUS_BM)))
        )
        self.medicine_del_btn = wx.BitmapButton(
            medicine_page, bitmap=wx.BitmapBundle(wx.Bitmap(str(MINUS_BM)))
        )
        self.medicine_list = medicine.List(medicine_page)

        service_page = wx.Panel(order_info)
        self.service_search = service.Picker(service_page)
        self.service_quantity = IntCtrl(service_page, min=0, limited=True)
        self.service_add_btn = wx.BitmapButton(
            service_page, bitmap=wx.BitmapBundle(wx.Bitmap(str(PLUS_BM)))
        )
        self.service_del_btn = wx.BitmapButton(
            service_page, bitmap=wx.BitmapBundle(wx.Bitmap(str(MINUS_BM)))
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
        self.visit_ok_btn = wx.Button(self, label="OK (CTRL+S)")
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
            static(self.visit_box, "Số ngày thuốc: "),
            (self.visit_days, 0, EA, 2),
            (0, 0, 3),
            static(self.visit_box, "Giá tiền: "),
            (self.visit_price, 0, EA, 2),
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

        row1 = row(
            static(medicine_page, "Thuốc: ", 100),
            (self.medicine_search, 1, EA, 2),
            static(medicine_page, "Ngày "),
            (self.medicine_times, 0, EA, 2),
            static(medicine_page, "lần, lần"),
            (self.medicine_dose, 0, EA, 2),
            (self.medicine_usage_unit, 0, wx.ALIGN_CENTER_VERTICAL, 2),
            (10, 0),
            static(medicine_page, "Tổng: "),
            (self.medicine_quantity, 0, EA, 2),
            (self.medicine_selling_unit, 0, wx.ALIGN_CENTER_VERTICAL, 2),
            (self.medicine_add_btn, 0, EA, 2),
            (self.medicine_del_btn, 0, EA, 2),
        )
        row2 = row(
            static(medicine_page, "Ghi chú:", 100),
            (self.medicine_usage_note, 0, EA, 2),
            (self.medicine_usage_note_txt, 0, wx.ALIGN_CENTER_VERTICAL, 2),
        )
        medicine_page.SetSizer(
            column((row1, 0, EA, 5), (row2, 0, EA, 5), (self.medicine_list, 1, EA, 5))
        )

        row1 = row(
            static(service_page, "Dịch vụ: ", 100),
            (self.service_search, 1, EA, 2),
            static(service_page, "Số lượng: "),
            (self.service_quantity, 0, EA, 2),
            (self.service_add_btn, 0, EA, 2),
            (self.service_del_btn, 0, EA, 2),
        )
        service_page.SetSizer(column((row1, 0, EA, 5), (self.service_list, 1, EA, 5)))

        left = column(
            (self.patient_search, 0, EA, 5),
            (patient_book, 2, EA, 5),
            (self.visit_list, 1, EA, 5),
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
        self._medicine: sqlite3.Row | None
        self._service: sqlite3.Row | None

        # navigation
        self.patient_gender.Bind(
            wx.EVT_KEY_DOWN,
            lambda e: (
                self.patient_birthdate.SetFocus()
                if e.KeyCode == wx.WXK_TAB and e.GetModifiers() == wx.MOD_NONE
                else e.Skip()
            ),
        )
        self.patient_past_history.Bind(
            wx.EVT_KEY_DOWN,
            lambda e: (
                self.patient_birthdate.SetFocus()
                if e.KeyCode == wx.WXK_TAB and e.GetModifiers() == wx.MOD_SHIFT
                else e.Skip()
            ),
        )

        # others
        self.patient_search.Bind(wx.EVT_SEARCH, self.on_patient_search)
        self.patient_birthdate.Bind(wx.adv.EVT_DATE_CHANGED, self.on_date_changed)

        # display_usage_note
        self.medicine_times.Bind(wx.EVT_TEXT, lambda _: self.display_usage_note())
        self.medicine_dose.Bind(wx.EVT_TEXT, lambda _: self.display_usage_note())
        self.medicine_usage_note.Bind(wx.EVT_TEXT, lambda _: self.display_usage_note())

        # calculate_medicine_quatity
        self.medicine_times.Bind(
            wx.EVT_TEXT, lambda _: self.calculate_medicine_quatity()
        )
        self.medicine_dose.Bind(
            wx.EVT_TEXT, lambda _: self.calculate_medicine_quatity()
        )

        # list buttons
        self.medicine_add_btn.Bind(wx.EVT_BUTTON, self.on_medicine_add_btn)
        self.medicine_del_btn.Bind(wx.EVT_BUTTON, self.on_medicine_del_btn)
        self.service_add_btn.Bind(wx.EVT_BUTTON, self.on_service_add_btn)
        self.service_del_btn.Bind(wx.EVT_BUTTON, self.on_service_del_btn)

        # buttons
        self.patient_new_btn.Bind(wx.EVT_BUTTON, self.on_patient_new_btn)
        self.patient_upd_btn.Bind(wx.EVT_BUTTON, self.on_patient_upd_btn)
        self.patient_ok_btn.Bind(wx.EVT_BUTTON, self.on_patient_ok_btn)
        self.patient_cancel_btn.Bind(wx.EVT_BUTTON, self.on_patient_cancel_btn)
        self.visit_new_btn.Bind(wx.EVT_BUTTON, self.on_visit_new_btn)
        self.visit_same_btn.Bind(wx.EVT_BUTTON, self.on_visit_same_btn)
        self.visit_upd_btn.Bind(wx.EVT_BUTTON, self.on_visit_upd_btn)
        self.visit_ok_btn.Bind(wx.EVT_BUTTON, self.on_visit_ok_btn)
        self.visit_cancel_btn.Bind(wx.EVT_BUTTON, self.on_visit_cancel_btn)

        # beginning state
        self.patient_edit_mode(False)
        self.visit_edit_mode(False)
        self.medicine_edit_mode(False)
        self.service_edit_mode(False)
        self.visit_days.ChangeValue(
            get_app().config["process"]["default_days_for_prescription"]
        )
        self.visit_price.SetInt(get_app().config["process"]["price"])
        self.patient_search.SetFocus()
        self.populate_seentoday()
        self.populate_follow_up()

        self.SetAcceleratorTable(
            wx.AcceleratorTable(
                [
                    wx.AcceleratorEntry(
                        wx.ACCEL_CTRL, ord("o"), accel_focus_search := wx.NewId()
                    ),
                    wx.AcceleratorEntry(
                        wx.ACCEL_CTRL, ord("n"), accel_new_patient := wx.NewId()
                    ),
                    wx.AcceleratorEntry(
                        wx.ACCEL_CTRL, ord("s"), accel_save_visit := wx.NewId()
                    ),
                ]
            )
        )
        self.Bind(
            wx.EVT_MENU, lambda _: self.patient_search.SetFocus(), id=accel_focus_search
        )
        self.Bind(wx.EVT_MENU, self.on_patient_new_btn, id=accel_new_patient)
        self.Bind(
            wx.EVT_MENU,
            lambda e: self.on_visit_ok_btn(e) if self.visit_ok_btn.IsShown() else ...,
            id=accel_save_visit,
        )

    @property
    def patient_id(self) -> int | None:
        return self._patient_id

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
            self.visit_list.DeleteAllItems()
            self.visit_id = None
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
                self.patient_name.ChangeValue(patient["name"])
                self.patient_gender.SetGender(patient["gender"])
                self.patient_birthdate.SetValue(patient["birthdate"])
                self.patient_past_history.SetValue(patient["past_history"])
                self.patient_upd_btn.Enable()
                for item in (
                    get_app()
                    .conn.execute(
                        """
                        SELECT id, exam_datetime, diagnosis FROM visits WHERE patient_id = ?
                        ORDER BY id DESC
                        """,
                        (value,),
                    )
                    .fetchall()
                ):
                    self.visit_list.append(item)

            except sqlite3.Error as error:
                wx.MessageBox(str(error), "Lỗi")

    @property
    def visit_id(self) -> int | None:
        return self._visit_id

    @visit_id.setter
    def visit_id(self, value: int | None):
        if value is None:
            self._visit_id = None
            self.visit_box.SetLabel("Thông tin lượt khám")
            self.visit_weight.SetInt(Decimal())
            self.visit_days.SetValue(
                get_app().config["process"]["default_days_for_prescription"]
            )
            self.visit_price.SetInt(get_app().config["process"]["price"])
            self.visit_medical_history.Clear()
            self.visit_diagnosis.Clear()
            self.visit_note.Clear()
            self.visit_same_btn.Disable()
            self.visit_upd_btn.Disable()
            self.medicine = None
            self.service = None
            self.medicine_list.DeleteAllItems()
            self.service_list.DeleteAllItems()
        else:
            self._visit_id = value
            visit = (
                get_app()
                .conn.execute(
                    """
                    SELECT weight, days, medical_history, diagnosis, note, price
                    FROM visits
                    WHERE id = ?
                    """,
                    (value,),
                )
                .fetchone()
            )
            self.visit_box.SetLabel(f"Thông tin lượt khám: {value}")
            self.visit_weight.SetInt(Decimal(visit["weight"]) / 10)
            self.visit_days.SetValue(visit["days"])
            self.visit_price.SetInt(visit["price"])
            self.visit_medical_history.ChangeValue(visit["medical_history"])
            self.visit_diagnosis.ChangeValue(visit["diagnosis"])
            self.visit_note.ChangeValue(visit["note"])
            self.visit_same_btn.Enable()
            self.visit_upd_btn.Enable()
            for item in (
                get_app()
                .conn.execute(
                    """
                    SELECT s.id, s.name, m.times, m.dose, m.quantity, m.usage_note, s.selling_unit, s.selling_price, s.usage_unit 
                    FROM (SELECT medicine_id, times, dose, quantity, usage_note FROM medicines WHERE visit_id=?) AS m
                    JOIN (SELECT id, name, selling_price, selling_unit, usage_unit FROM medicine_store) AS s
                    WHERE s.id = m.medicine_id
                    """,
                    (value,),
                )
                .fetchall()
            ):
                self.medicine_list.append(item)
            for item in (
                get_app()
                .conn.execute(
                    """
                    SELECT s.id, s.name, m.quantity, s.price
                    FROM (SELECT service_id, quantity FROM services WHERE visit_id=?) AS m
                    JOIN (SELECT id, name, price FROM service_store) AS s
                    WHERE s.id = m.service_id
                    """,
                    (value,),
                )
                .fetchall()
            ):
                self.service_list.append(item)

    @property
    def medicine(self) -> sqlite3.Row | None:
        return self._medicine

    @medicine.setter
    def medicine(self, value: sqlite3.Row | None):
        if value is None:
            self.medicine_search.ChangeValue("")
            self.medicine_usage_unit.SetLabel("{đơn vị}")
            self.medicine_selling_unit.SetLabel("{đơn vị}")
            self.medicine_times.ChangeValue(0)  # pyright: ignore[reportArgumentType]
            self.medicine_dose.ChangeValue("")
            self.medicine_quantity.ChangeValue(0)  # pyright: ignore[reportArgumentType]
            self.medicine_usage_note.ChangeValue("")
            self.medicine_usage_note_txt.SetLabel("")
            self.medicine_edit_mode(False)
        else:
            self.medicine_search.ChangeValue(value["name"])
            self.medicine_usage_unit.SetLabel(value["usage_unit"])
            self.medicine_selling_unit.SetLabel(value["selling_unit"])
            self.medicine_edit_mode()

    @property
    def service(self) -> sqlite3.Row | None:
        return self._service

    @service.setter
    def service(self, value: sqlite3.Row | None):
        if value is None:
            self.service_search.ChangeValue("")
            self.service_quantity.ChangeValue(0)  # pyright: ignore[reportArgumentType]
            self.service_edit_mode(False)
        else:
            self.service_search.ChangeValue(value["name"])
            self.service_edit_mode()

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
        self.medicine_times.Enable(b)
        self.medicine_dose.Enable(b)
        self.medicine_quantity.Enable(b)
        self.medicine_usage_note.Enable(b)
        self.medicine_add_btn.Enable(b)
        self.medicine_del_btn.Enable(b)

    def service_edit_mode(self, b: bool = True):
        self.service_quantity.Enable(b)
        self.service_add_btn.Enable(b)
        self.service_del_btn.Enable(b)

    def refresh(self):
        self.patient_id = None
        self.visit_id = None
        self.medicine = None
        self.service = None
        self.populate_queue(self.patient_search.Value.strip())
        self.populate_seentoday()
        self.populate_follow_up()
        self.populate_visit_list()

    def populate_queue(self, value: str = ""):
        self.queue.DeleteAllItems()
        for item in get_app().conn.execute(
            """
            SELECT id, name, gender, birthdate from patients
            WHERE name LIKE ?
            """,
            ("%" + value.upper() + "%",),
        ):
            self.queue.append(item)

    def populate_seentoday(self):
        self.seentoday.DeleteAllItems()
        for item in get_app().conn.execute("SELECT * FROM seentoday"):
            self.seentoday.append(item)

    def populate_follow_up(self):
        self.follow_up.DeleteAllItems()
        for item in get_app().conn.execute("SELECT * FROM follow_up"):
            self.follow_up.append(item)

    def populate_visit_list(self):
        self.visit_list.DeleteAllItems()
        if self.patient_id is not None:
            for item in (
                get_app()
                .conn.execute(
                    """
                        SELECT id, exam_datetime, diagnosis FROM visits WHERE patient_id = ?
                        ORDER BY id DESC
                        """,
                    (self.patient_id,),
                )
                .fetchall()
            ):
                self.visit_list.append(item)

    def on_patient_search(self, e: wx.CommandEvent):
        self.populate_queue(e.String.strip().upper())

    def on_medicine_add_btn(self, _):
        assert self.medicine is not None
        self.medicine_list.Append(
            [
                str(self.medicine_list.ItemCount + 1),
                self.medicine["id"],
                self.medicine["name"],
                self.medicine_times.Value.strip(),
                f"{self.medicine_dose.Value.strip()} {self.medicine['usage_unit']}",
                f"{self.medicine_quantity.Value.strip()} {self.medicine['selling_unit']}",
                self.medicine_usage_note.Value.strip(),
                str(self.medicine["selling_price"] * self.medicine_quantity.Value),
            ]
        )
        self.medicine = None

    def on_medicine_del_btn(self, _):
        i = self.medicine_list.GetFirstSelected()
        assert i != wx.NOT_FOUND
        self.medicine_list.DeleteItem(i)
        for i in range(self.medicine_list.ItemCount):
            self.medicine_list.SetItem(i, 0, str(i + 1))
        self.medicine = None

    def on_service_add_btn(self, _):
        assert self.service is not None
        self.service_list.Append(
            [
                str(self.service_list.ItemCount + 1),
                self.service["id"],
                self.service["name"],
                str(self.service_quantity.Value),
                str(self.service["price"] * self.service_quantity.Value),
            ]
        )
        self.service = None

    def on_service_del_btn(self, _):
        i = self.service_list.GetFirstSelected()
        assert i != wx.NOT_FOUND
        self.service_list.DeleteItem(i)
        for i in range(self.service_list.ItemCount):
            self.service_list.SetItem(i, 0, str(i + 1))
        self.service = None

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
            wx.MessageBox(str(error), "Lỗi")
        finally:
            self.patient_edit_mode(False)

    def on_patient_cancel_btn(self, _):
        id = self.patient_id
        if id is None:
            self.patient_id = None
        else:
            self.patient_id = id
        self.patient_edit_mode(False)

    def on_visit_new_btn(self, _):
        if self.patient_id is not None:
            self.visit_id = None
            self.visit_edit_mode()
            last_weight = (
                get_app()
                .conn.execute(
                    """
                        SELECT weight FROM visits WHERE patient_id = ?
                        ORDER BY exam_datetime DESC
                        LIMIT 1
                        """,
                    (self.patient_id,),
                )
                .fetchone()["weight"]
            )

            if last_weight:
                self.visit_weight.SetInt(Decimal(last_weight) / 10)
            else:
                self.visit_weight.SetInt(Decimal())

    def on_visit_same_btn(self, _):
        if self.patient_id is not None:
            self._visit_id = None
            self.visit_edit_mode()

    def on_visit_upd_btn(self, _):
        if self.patient_id is not None:
            self.visit_edit_mode()

    def on_visit_ok_btn(self, _):
        if self.patient_id is not None:
            id = self.visit_id
            visit = Visit(
                patient_id=self.patient_id,
                weight=int(self.visit_weight.GetInt() * 10),
                medical_history=self.visit_medical_history.Value.strip(),
                diagnosis=self.visit_diagnosis.Value.strip(),
                days=int(self.visit_days.Value),
                note=self.visit_note.Value.strip(),
                price=self.visit_price.GetInt(),
            )
            try:
                if id is None:
                    id = insert(get_app().conn, visit)
                    self._visit_id = id
                    for item in self.medicine_list.to_model():
                        insert(get_app().conn, item)
                    for item in self.service_list.to_model():
                        insert(get_app().conn, item)
                else:
                    update(get_app().conn, visit, id)
                    get_app().conn.execute(
                        "DELETE FROM medicines WHERE visit_id = ?", (id,)
                    )
                    get_app().conn.execute(
                        "DELETE FROM services WHERE visit_id = ?", (id,)
                    )
                    for item in self.medicine_list.to_model():
                        insert(get_app().conn, item)
                    for item in self.service_list.to_model():
                        insert(get_app().conn, item)
            except sqlite3.Error as error:
                wx.MessageBox(str(error), "Lỗi")
            finally:
                self.populate_visit_list()
                self.visit_edit_mode(False)

    def on_visit_cancel_btn(self, _):
        if self.patient_id is not None:
            id = self.visit_id
            if id is None:
                self.visit_id = None
            else:
                self.visit_id = id
            self.visit_edit_mode(False)

    def on_date_changed(self, e: wx.adv.DateEvent):
        self.patient_age.ChangeValue(bd_to_vn_age(e.GetDate()))

    def display_usage_note(self):
        assert self.medicine is not None
        if self.medicine_times.Value != "" and self.medicine_dose.Value != "":
            self.medicine_usage_note_txt.SetLabel(
                "{} ngày {} lần, lần {} {} ({})".format(
                    self.medicine["route"],
                    self.medicine_times.Value.strip(),
                    self.medicine_dose.Value.strip(),
                    self.medicine["usage_unit"],
                    self.medicine_usage_note.Value.strip(),
                )
            )

    def calculate_medicine_quatity(self):
        assert self.medicine is not None
        if self.medicine_times.Value != "" and self.medicine_dose.Value != "":
            if self.medicine["selling_unit"] != self.medicine["usage_unit"]:
                self.medicine_quantity.ChangeValue(1)  # pyright: ignore[reportArgumentType]
            else:
                if "/" in self.medicine_dose.Value:
                    try:
                        numer, denom = [
                            int(i)
                            for i in self.medicine_dose.Value.strip().split("/", 1)
                        ]
                        self.medicine_quantity.ChangeValue(
                            ceil(
                                self.medicine_times.Value  # pyright: ignore[reportOperatorIssue]
                                * Fraction(numer, denom)
                                * self.visit_days.Value
                            )
                        )
                    except Exception:
                        self.medicine_quantity.ChangeValue(0)  # pyright: ignore[reportArgumentType]
                else:
                    self.medicine_quantity.ChangeValue(
                        ceil(
                            self.medicine_times.Value  # pyright: ignore[reportOperatorIssue]
                            * float(self.medicine_dose.Value.strip())
                            * self.visit_days.Value
                        )
                    )
