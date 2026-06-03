import wx
from lib.db import insert, update
from typing import override, cast
from simpleclinic import service_store_frame
from ._dialog import Dialog
import sqlite3
from lib.wx_helper import get_app


class AddDialog(Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Thêm dịch vụ")

    @override
    def on_ok(self, _):
        item = self.get_item()
        try:
            with get_app().conn as conn:
                insert(conn, item)
            get_app().fetch_service_store()
            cast(service_store_frame.StoreFrame, self.Parent).refresh()
            self.Close()
        except sqlite3.Error as error:
            wx.MessageBox(str(error), "Thêm mới thất bại")


class UpdateDialog(Dialog):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, title="Cập nhật dịch vụ", *args, **kwargs)

    @override
    def on_ok(self, _):
        assert isinstance(self.id, int)
        item = self.get_item()
        try:
            with get_app().conn as conn:
                update(conn, item, self.id)
            get_app().fetch_service_store()
            cast(service_store_frame.StoreFrame, self.Parent).refresh()
            self.Close()
        except sqlite3.Error as error:
            wx.MessageBox(str(error), "Cập nhật thất bại")
