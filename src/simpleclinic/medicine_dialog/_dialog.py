import wx
from wx.lib.intctrl import IntCtrl
from lib.wx_helper import EA, row, column
from lib.db.models import MedicineStore
from lib.wx_helper.widget import ThousandGroupIntCtrl


class Dialog(wx.Dialog):
    def __init__(
        self,
        parent: wx.Window,
        title: str,
        id: int | None = None,
        name="",
        element="",
        quantity=0,
        route="",
        usage_unit="",
        selling_unit="",
        cost_price=0,
        selling_price=0,
    ):
        super().__init__(
            parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        self.name = wx.TextCtrl(
            self,
            name="Tên thuốc",
        )
        self.element = wx.TextCtrl(self, name="Thành phần", size=wx.Size(300, -1))
        self.quantity = IntCtrl(self, name="Số lượng", min=0, limited=True)
        self.route = wx.TextCtrl(self, name="Đường dùng")
        self.usage_unit = wx.TextCtrl(self, name="Đơn vị dùng")
        self.selling_unit = wx.TextCtrl(self, name="Đơn vị bán")
        self.cost_price = ThousandGroupIntCtrl(self, name="Giá mua")
        self.selling_price = ThousandGroupIntCtrl(self, name="Giá bán")
        self.ok_btn = wx.Button(self, label="Ok")
        self.cancel_btn = wx.Button(self, label="Cancel")

        def widget(w: wx.TextCtrl):
            left = wx.ALIGN_CENTER_VERTICAL | wx.ALL
            right = wx.EXPAND | wx.ALL
            return (wx.StaticText(self, label=w.Name), 0, left, 3), (w, 1, right, 3)

        info_sizer = wx.FlexGridSizer(11, 2, 3, 3)
        info_sizer.AddGrowableCol(1, 3)
        info_sizer.AddMany(
            [
                *widget(self.name),
                *widget(self.element),
                *widget(self.quantity),
                *widget(self.route),
                *widget(self.usage_unit),
                *widget(self.selling_unit),
                *widget(self.cost_price),
                *widget(self.selling_price),
            ]
        )
        btn_sizer = row(
            (0, 0, 1),
            (self.ok_btn, 0, wx.ALL, 5),
            (self.cancel_btn, 0, wx.ALL, 5),
        )

        self.SetSizerAndFit(
            column(
                (info_sizer, 1, EA, 5),
                (btn_sizer, 0, EA, 5),
            )
        )

        self.id = id
        self.name.ChangeValue(name)
        self.element.ChangeValue(element)
        self.quantity.ChangeValue(quantity)  # pyright: ignore[reportArgumentType]
        self.route.ChangeValue(route)
        self.usage_unit.ChangeValue(usage_unit)
        self.selling_unit.ChangeValue(selling_unit)
        self.cost_price.SetInt(cost_price)
        self.selling_price.SetInt(selling_price)

        self.ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_ok(self, _): ...
    def on_cancel(self, _):
        self.Close()

    def get_item(self):
        return MedicineStore(
            name=self.name.Value.strip(),
            element=self.element.Value.strip(),
            quantity=int(self.quantity.Value),
            route=self.route.Value.strip(),
            usage_unit=self.usage_unit.Value.strip(),
            selling_unit=self.selling_unit.Value.strip(),
            cost_price=self.cost_price.GetInt(),
            selling_price=self.selling_price.GetInt(),
        )
