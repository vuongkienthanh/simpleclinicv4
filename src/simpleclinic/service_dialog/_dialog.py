import wx
from wx.lib.intctrl import IntCtrl
from lib.wx_helper import EA, row, column
from lib.models import ServiceStore


class Dialog(wx.Dialog):
    def __init__(
        self, parent: wx.Window, title: str, id: int | None = None, name="", price=""
    ):
        super().__init__(
            parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        self.name = wx.TextCtrl(self, name="Dịch vụ")
        self.price = IntCtrl(self, name="Giá", min=0, limited=True)
        self.okbtn = wx.Button(self, label="Ok")
        self.cancelbtn = wx.Button(self, label="Cancel")

        def widget(w: wx.TextCtrl):
            left = wx.ALIGN_CENTER_VERTICAL | wx.ALL
            right = wx.EXPAND | wx.ALL
            return (wx.StaticText(self, label=w.Name), 0, left, 3), (w, 1, right, 3)

        info_sizer = wx.FlexGridSizer(2, 2, 3, 3)
        info_sizer.AddGrowableCol(1, 3)
        info_sizer.AddMany(
            [
                *widget(self.name),
                *widget(self.price),
            ]
        )
        btn_sizer = row(
            (0, 0, 1),
            (self.okbtn, 0, wx.ALL, 5),
            (self.cancelbtn, 0, wx.ALL, 5),
        )

        self.SetSizerAndFit(
            column(
                (info_sizer, 1, EA, 5),
                (btn_sizer, 0, EA, 5),
            )
        )

        self.id = id
        self.name.ChangeValue(name)
        self.price.ChangeValue(price)

        self.okbtn.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancelbtn.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_ok(self, _): ...
    def on_cancel(self, _):
        self.Close()

    def get_item(self):
        return ServiceStore(
            name=self.name.Value.strip(),
            price=int(self.price.Value),
        )
