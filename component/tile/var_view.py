from sepal_ui import sepalwidgets as sw
from sepal_ui.scripts import utils as su

from component import widget as cw
from component import parameter as cp


class VarView(sw.Tile):

    nb_custom = 0
    "number of custom var widget set in"

    def __init__(self, model):

        # gather the model
        self.model = model

        # the default variables
        default_title = sw.Html(tag="h2", children=["Default"])
        default_vars = [cw.DefaultVar(str(k)) for k in cp.default_datasets]

        # the custom ones
        custom_title = sw.Html(tag="h2", children=["Custom"])
        self.custom_add = sw.Btn(
            small=True,
            text="Add custom dataset",
            icon="fas fa-plus",
            color="success",
            rounded=True,
        )

        # create the view
        self.content = [default_title, *default_vars, custom_title, self.custom_add]
        super().__init__("nested", "no_title", inputs=self.content)

        # nest the tile
        self.nest()

        # add js behaviour
        self.custom_add.on_event("click", self.add_var)

    @su.switch("loading", on_widgets=["custom_add"])
    def add_var(self, event, widget, data):
        """add a variable to the list"""
        custom = cw.CustomVar()
        custom.btn.id = self.nb_custom + 1
        self.nb_custom += 1
        self.content += [custom]
        self.set_content(self.content)

        # add the js behaviour of the delete buttom
        custom.btn.on_event("click", self.remove_custom)

        return

    @su.switch("loading", on_widgets=["custom_add"])
    def remove_custom(self, widget, event, data):

        # get the id from the btn
        id_ = widget.id

        # reomve them from content
        custom = next(
            c for c in self.content if isinstance(c, cw.CustomVar) and c.btn.id == id_
        )
        self.content.remove(custom)

        self.set_content(self.content)

        return
