import wx
from ._dialog import Dialog
from lib.db import insert, update
from typing import override
import sqlite3
from lib.wx_helper import get_app


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
            self.Close()
        except sqlite3.Error as error:
            wx.MessageBox("Thêm mới thất bại", f"{error}")


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
            self.Close()
        except sqlite3.Error as error:
            wx.MessageBox("Cập nhật thất bại", f"{error}")
