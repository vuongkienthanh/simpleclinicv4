import wx
from ._dialog import Dialog
from lib.db import insert, update
from typing import override, cast
import sqlite3
from lib.wx_helper import get_app
from simpleclinic import medicine_store_frame


class AddDialog(Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Thêm thuốc mới")

    @override
    def on_ok(self, _):
        item = self.get_item()
        app = get_app()
        try:
            insert(app.conn, item)
            app.fetch_medicine_store()
            cast(medicine_store_frame.StoreFrame, self.Parent).refresh()
            self.Close()
        except sqlite3.Error as error:
            wx.MessageBox(str(error), "Thêm mới thất bại")


class UpdateDialog(Dialog):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, title="Cập nhật thuốc", *args, **kwargs)

    @override
    def on_ok(self, _):
        assert isinstance(self.id, int)
        item = self.get_item()
        app = get_app()
        try:
            update(app.conn, item, self.id)
            app.fetch_medicine_store()
            cast(medicine_store_frame.StoreFrame, self.Parent).refresh()
            self.Close()
        except sqlite3.Error as error:
            wx.MessageBox(str(error), "Cập nhật thất bại")
