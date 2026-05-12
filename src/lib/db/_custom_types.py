from lib.enums import Gender
import sqlite3
import wx

DATE_FORMAT = "%d/%m/%Y"

def custom_type_date():
    def adapt(date: wx.DateTime) -> str:
        return date.Format(DATE_FORMAT)

    def convert(b: bytes) -> wx.DateTime:
        d = wx.DateTime()
        d.ParseFormat(b.decode(), format=DATE_FORMAT)
        return d

    sqlite3.register_adapter(wx.DateTime, adapt)
    sqlite3.register_converter("DATE", convert)


def custom_type_datetime():
    def adapt(datetime: wx.DateTime) -> str:
        return datetime.FormatISOCombined()

    def convert(b: bytes) -> wx.DateTime:
        d = wx.DateTime()
        d.ParseISOCombined(b.decode())
        return d

    sqlite3.register_adapter(wx.DateTime, adapt)
    sqlite3.register_converter("TIMESTAMP", convert)


def custom_type_gender():
    def adapt(gender: Gender) -> int:
        return gender.value

    def convert(b: bytes) -> Gender:
        return Gender(int(b))

    sqlite3.register_adapter(Gender, adapt)
    sqlite3.register_converter("GENDER", convert)
