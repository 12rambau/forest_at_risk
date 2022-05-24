from sepal_ui import sepalwidgets as sw
import ipyvuetify as v
from traitlets import Bool

from component import parameter as cp


class DefaultVar(sw.Card):

    colors = ["", "success"]

    active = Bool(True).tag(sync=True)
    "bool: the state of the variable field"

    def __init__(self, layername):

        # set the name
        self.title = sw.TextField(v_model=layername, readonly=True)
        flex_title = sw.Flex(xs5=True, children=[self.title, sw.Spacer()])

        # get the different way a variable can be used
        self.select = sw.Select(
            xs5=True, class_="mx-3", items=cp.operators, label="use", v_model=None
        )

        # get the btn
        self.icon = sw.Icon(
            x_small=True, children=["fas fa-check"], color=self.colors[self.active]
        )
        self.btn = v.Btn(
            children=[self.icon], color="secondary", x_small=True, fab=True
        )
        btn_flex = sw.Flex(xs2=True, children=[self.btn])

        # wrap everything in a horizontal layout
        layout = sw.Layout(
            row=True,
            class_="align-center ml-3 mr-3",
            children=[flex_title, self.select, sw.Spacer(), self.btn],
        )

        super().__init__(children=[layout], class_="d-block flex-wrap ma-2")

        # add js behaviour
        self.btn.on_event("click", self.toggle_selection)

    def toggle_selection(self, widget, event, data):

        self.active = not self.active

        # change the icon
        icon = sw.Icon(x_small=True, children=[self.icons[self.active]])
        self.icon.color = self.colors[self.active]

        # change the state of all the layers
        self.select.disabled = not self.active
        self.title.disabled = not self.active

        return


class CustomVar(sw.Card):

    colors = ["", "success"]
    icons = ["fas fa-check", "fas fa-trash-alt"]

    def __init__(self):

        # set the name
        self.title = sw.FileInput(extentions=[".tif", ".tiff", ".vrt"])
        flex_title = sw.Flex(xs5=True, children=[self.title, sw.Spacer()])

        # get the different way a variable can be used
        self.select = sw.Select(
            xs5=True, class_="mx-3", items=cp.operators, label="use", v_model=None
        )

        # get the btn
        icon = sw.Icon(x_small=True, children=["fas fa-trash-alt"])
        self.btn = v.Btn(children=[icon], color="secondary", x_small=True, fab=True)
        btn_flex = sw.Flex(xs2=True, children=[self.btn])

        # wrap everything in a horizontal layout
        layout = sw.Layout(
            row=True,
            class_="align-center ml-3 mr-3",
            children=[flex_title, self.select, sw.Spacer(), self.btn],
        )

        super().__init__(children=[layout], class_="d-block flex-wrap ma-2")
