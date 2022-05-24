from sepal_ui import sepalwidgets as sw

from component import widget as cw


class VarView(sw.Tile):
    def __init__(self, model):

        # gather the model
        self.model = model

        # fill the children attribute step by step
        children = []

        # the default variables
        default_title = sw.Html(tag="h2", children=["Default"])
        default_vars = [cw.DefaultVar(str(i)) for i in range(3)]

        # the custom ones
        custom_title = sw.Html(tag="h2", children=["Custom"])
        custom_add = sw.Btn(
            small=True,
            text="Add custom dataset",
            icon="fas fa-plus",
            color="success",
            rounded=True,
        )

        # create the view
        children = [default_title, *default_vars, custom_title, custom_add]
        super().__init__("nested", "no_title", inputs=children)

        # nest the tile
        self.nest()
