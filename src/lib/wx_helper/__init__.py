import wx
from typing import cast
import simpleclinic

EA = wx.EXPAND | wx.ALL


def get_app() -> simpleclinic.App:
    return cast(simpleclinic.App, wx.App.Get())


def get_main_frame() -> simpleclinic.MainFrame:
    return cast(simpleclinic.MainFrame, wx.App.GetMainTopWindow())


def column(*children) -> wx.BoxSizer:
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.AddMany([child for child in children])
    return sizer


def row(*children) -> wx.BoxSizer:
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.AddMany([child for child in children])
    return sizer


SPECIALS = [
    wx.WXK_BACK,
    wx.WXK_DELETE,
    wx.WXK_HOME,
    wx.WXK_END,
    wx.WXK_LEFT,
    wx.WXK_RIGHT,
    wx.WXK_TAB,
    wx.WXK_RETURN,
    1,  # ctrl-a
    3,  # ctrl-c
    22,  # ctrl-v
]
NUMBERS = list(range(48, 58))
NUMPADS = [
    wx.WXK_NUMPAD0,
    wx.WXK_NUMPAD1,
    wx.WXK_NUMPAD2,
    wx.WXK_NUMPAD3,
    wx.WXK_NUMPAD4,
    wx.WXK_NUMPAD5,
    wx.WXK_NUMPAD6,
    wx.WXK_NUMPAD7,
    wx.WXK_NUMPAD8,
    wx.WXK_NUMPAD9,
]
SLASH = [47]
DECIMAL = [46]
