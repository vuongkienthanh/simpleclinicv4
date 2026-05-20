from lib.enums import Gender
import sqlite3
import wx


def custom_type_datetime():

    def convert_datetime(b: bytes) -> wx.DateTime:
        d = wx.DateTime()
        d.ParseISOCombined(b.decode())
        return d

    def convert_date(b: bytes) -> wx.DateTime:
        d = wx.DateTime()
        d.ParseISODate(b.decode())
        return d

    sqlite3.register_converter("DATETIME", convert_datetime)
    sqlite3.register_converter("DATE", convert_date)


def custom_type_gender():
    def adapt(gender: Gender) -> int:
        return gender.value

    def convert(b: bytes) -> Gender:
        return Gender(int(b))

    sqlite3.register_adapter(Gender, adapt)
    sqlite3.register_converter("GENDER", convert)
