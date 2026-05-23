import datetime as dt
import textwrap

import wx
import wx.adv
from lib import DATE_FORMAT
from lib.wx_helper import get_app, get_main_frame
from lib.paths import APP_DIR, LOGO, PRESCRIPTION_OUTPUT
from lib.vn import bd_to_age
from ._printer import replace_prescription


class MenuBar(wx.MenuBar):
    def __init__(self):
        super().__init__()

        home = wx.Menu()
        home.Append(wx.ID_REFRESH, "&Refresh\tF5")
        home.Append(wx.ID_ABOUT)
        home.Append(wx.ID_EXIT, "&Exit\tCTRL+Q")
        self.Bind(wx.EVT_MENU, lambda _: get_app().refresh(), id=wx.ID_REFRESH)
        self.Bind(wx.EVT_MENU, self.onAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, lambda _: get_main_frame().Close(), id=wx.ID_EXIT)

        edit = wx.Menu()
        self.new_patient = edit.Append(wx.ID_ANY, "Bệnh nhân mới\tCTRL+N")
        self.new_visit = edit.Append(wx.ID_ANY, "Lượt khám mới\tCTRL+M")
        self.Bind(
            wx.EVT_MENU, get_main_frame().on_patient_new_btn, source=self.new_patient
        )
        self.Bind(wx.EVT_MENU, get_main_frame().on_visit_new_btn, source=self.new_visit)

        edit.AppendSeparator()

        edit.Append(wx.ID_PRINT, "In\tCTRL+P")
        edit.Append(wx.ID_INFO, "Copy thông tin lượt khám\tCTRL+SHIFT+C")
        self.Bind(wx.EVT_MENU, self.on_print, id=wx.ID_PRINT)
        self.Bind(wx.EVT_MENU, self.on_copy_info, id=wx.ID_INFO)

        stores = wx.Menu()
        medicine_store = stores.Append(wx.ID_ANY, "Kho thuốc")
        service_store = stores.Append(wx.ID_ANY, "Thủ thuật")
        self.Bind(wx.EVT_MENU, self.on_medicine_store, medicine_store)
        self.Bind(wx.EVT_MENU, self.on_service_store, service_store)

        # menuReport = wx.Menu()
        # menuDayReport = menuReport.Append(wx.ID_ANY, "Số lượng bệnh theo ngày")
        # menuMonthReport = menuReport.Append(wx.ID_ANY, "Số lượng bệnh theo tháng")
        # menuMonthWarehouseReport = menuReport.Append(
        #     wx.ID_ANY, "Tình hình dùng thuốc theo tháng"
        # )
        # manageMenu.AppendSubMenu(menuReport, "Báo cáo")

        setting = wx.Menu()

        open_config_folder = setting.Append(wx.ID_ANY, "Mở folder cài đặt + dữ liệu")
        self.Bind(wx.EVT_MENU, self.on_open_config_folder, open_config_folder)

        self.Append(home, "&Home")
        self.Append(edit, "&Khám bệnh")
        self.Append(stores, "&Quản lý")
        self.Append(setting, "&Hệ thống")

    def onAbout(self, _):
        info = wx.adv.AboutDialogInfo()
        info.SetName(get_app().AppDisplayName)
        info.SetVersion(get_app().version)
        info.SetCopyright(get_app().VendorDisplayName)
        info.SetIcon(wx.Icon(str(LOGO)))
        info.SetWebSite(get_app().url)
        wx.adv.AboutBox(info)

    def on_print(self, _): 
        replace_prescription()
        wx.LaunchDefaultApplication(str(PRESCRIPTION_OUTPUT))

    def on_copy_info(self, _):
        if wx.TheClipboard.Open():
            t = textwrap.dedent(
                """
            {}
            {} ({} {} {})
            Chẩn đoán: {}
            Thuốc {} ngày:
            {}
            Thủ thuật:
            {}
            Dặn dò: {}
            Tiền khám: {}
            """.format(
                    dt.datetime.now().strftime("%d/%m/%Y %H:%M"),
                    f"{get_main_frame().patient_name.Value}",
                    f"{get_main_frame().patient_gender.GetGender().display_name}",
                    f"{get_main_frame().patient_birthdate.Value.Format(DATE_FORMAT)}",
                    f"{bd_to_age(get_main_frame().patient_birthdate.Value)}",
                    get_main_frame().visit_diagnosis.Value,
                    get_main_frame().visit_days.Value,
                    "\n".join(
                        [
                            "{}/ {} {} x {} = {} ({})".format(
                                i + 1,
                                get_main_frame().medicine_list.GetItemText(i, 2),
                                get_main_frame().medicine_list.GetItemText(i, 5),
                                get_main_frame().medicine_list.GetItemText(i, 6),
                                get_main_frame().medicine_list.GetItemText(i, 7),
                                get_main_frame().medicine_list.GetItemText(i, 8),
                            )
                            for i in range(get_main_frame().medicine_list.ItemCount)
                        ]
                    ),
                    "\n".join(
                        [
                            "{}/ {} x {}".format(
                                i + 1,
                                get_main_frame().service_list.GetItemText(i, 2),
                                get_main_frame().service_list.GetItemText(i, 3),
                            )
                            for i in range(get_main_frame().service_list.ItemCount)
                        ]
                    ),
                    get_main_frame().visit_note.Value,
                    get_main_frame().visit_price.Value,
                )
            ).strip()
            wx.TheClipboard.SetData(wx.TextDataObject(t))
            wx.TheClipboard.Close()

    def on_medicine_store(self, _):
        from simpleclinic import medicine_store_frame

        medicine_store_frame.StoreFrame().Show()

    def on_service_store(self, _):
        from simpleclinic import service_store_frame

        service_store_frame.StoreFrame().Show()

    def on_open_config_folder(self, _):
        wx.LaunchDefaultApplication(str(APP_DIR))
