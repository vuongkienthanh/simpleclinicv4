import wx
from wx.lib.intctrl import IntCtrl
from lib.wx_helper import row, EA, NUMBERS, NUMPADS, SPECIALS, SLASH, DECIMAL, column


class Panel(wx.Panel):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self.search = wx.SearchCtrl(self)
        self.search.SetHint("Enter để search")
        self.times = IntCtrl(self, min=0, limited=True)
        self.dose = DoseCtrl(self)
        self.usage_unit = wx.StaticText(self, label="{đơn vị}")
        self.quantity = IntCtrl(self, min=0, limited=True)
        self.selling_unit = wx.StaticText(self, label="{đơn vị}")
        self.usage_note = wx.TextCtrl(self)
        self.list = ListCtrl(self)

        def static(label, width=-1):
            return (
                wx.StaticText(self, label=label, size=wx.Size(width, -1)),
                0,
                wx.ALIGN_CENTER_VERTICAL,
                0,
            )

        row1 = row(
            static("Thuốc: ", 100),
            (self.search, 1, EA, 2),
            static("Ngày "),
            (self.times, 0, EA, 2),
            static("lần, lần"),
            (self.dose, 0, EA, 2),
            (self.usage_unit, 0, wx.ALIGN_CENTER_VERTICAL, 2),
            static("Tổng: "),
            (self.quantity, 0, EA, 2),
            (self.selling_unit, 0, wx.ALIGN_CENTER_VERTICAL, 2),
        )
        row2 = row(
            static("Cách sử dụng:", 120),
            (self.usage_note, 1, EA, 2),
        )
        self.SetSizerAndFit(
            column((row1, 0, EA, 5), (row2, 0, EA, 5), (self.list, 1, EA, 5))
        )


class DoseCtrl(wx.TextCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self.Bind(wx.EVT_CHAR, self.on_char)

    def on_char(self, e: wx.KeyEvent):
        keys = NUMBERS + NUMPADS + SPECIALS
        s = self.Value
        if "/" not in s and "." not in s:
            keys += SLASH + DECIMAL

        if e.KeyCode in keys:
            e.Skip()


class ListCtrl(wx.ListCtrl):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, style=wx.LC_REPORT)
        self.AppendColumn("STT", width=-1)
        self.AppendColumn("Mã", width=-1)
        self.AppendColumn("Thuốc", width=-1)
        self.AppendColumn("Thành phần", width=-1)
        self.AppendColumn("Số Lần", width=-1)
        self.AppendColumn("Mỗi lần", width=-1)
        self.AppendColumn("Số lượng", width=-1)
        self.AppendColumn("Cách sử dụng", width=300)
        self.AppendColumn("Giá", width=-1)

    # def append(self, item: sqlite3.Row):
    #     self.Append(
    #         [
    #             str(item["id"]),
    #             item["exam_datetime"],
    #             item["diagnosis"],
    #         ]
    #     )
