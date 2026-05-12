import wx
from lib.wx_helper import EA, row, get_app
from wx.lib.intctrl import IntCtrl
from wx.lib.masked.numctrl import NumCtrl
from lib.paths import WEIGHT_BM


class Box(wx.Panel):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        sz = wx.StaticBoxSizer(wx.VERTICAL, self, label="Thông tin lượt khám")
        box = sz.GetStaticBox()
        self.weight = NumCtrl(box, fractionWidth=1, min=0, limited=True)
        self.get_weight = wx.BitmapButton(
            box, bitmap=wx.BitmapBundle(wx.Bitmap(str(WEIGHT_BM)))
        )
        self.get_weight.SetToolTip("Lấy cân nặng mới nhất")
        self.days = IntCtrl(
            box,
            value=get_app().config["process"]["default_days_for_prescription"],
            min=0,
            limited=True,
        )
        self.price = IntCtrl(box, min=0, limited=True)
        self.price_txt = wx.StaticText(box, label="", size=wx.Size(100, -1))
        self.medical_history = wx.TextCtrl(box, style=wx.TE_MULTILINE)
        self.diagnosis = wx.TextCtrl(box)
        self.note = wx.TextCtrl(box)

        def static(label: str, w=-1):
            return (
                wx.StaticText(box, label=label, size=wx.Size(w, -1)),
                0,
                wx.ALIGN_CENTER_VERTICAL,
                0,
            )

        row1 = row(
            static("Cân nặng: ", 100),
            (self.weight, 0, EA, 2),
            (self.get_weight, 0, EA, 2),
            static("Số ngày thuốc: "),
            (self.days, 0, EA, 2),
            (0, 0, 3),
            static("Giá tiền: "),
            (self.price, 0, EA, 2),
            (self.price_txt, 0, wx.ALIGN_CENTER_VERTICAL, 0),
        )
        row2 = row(
            static("Bệnh sử: ", 100),
            (self.medical_history, 1, EA, 0),
        )
        row3 = row(
            static("Chẩn đoán: ", 100),
            (self.diagnosis, 1, EA, 0),
        )
        row4 = row(
            static("Ghi chú: ", 100),
            (self.note, 1, EA, 0),
        )

        sz.AddMany(
            [
                (row1, 0, EA, 5),
                (row2, 1, EA, 5),
                (row3, 0, EA, 5),
                (row4, 0, EA, 5),
            ]
        )
        self.SetSizerAndFit(sz)
        self.SetOwnBackgroundColour(wx.Colour(230, 239, 254))

        self.Bind(wx.EVT_TEXT, self.on_price_changed, source=self.price)

    def on_price_changed(self, e):
        self.price_txt.SetLabel(f"{int(e.String):,}")
