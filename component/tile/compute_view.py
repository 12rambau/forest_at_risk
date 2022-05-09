from sepal_ui import sepalwidgets as sw


class ComputeView(sw.Tile):
    def __init__(self, model):

        # gather the model
        self.model = model

        # create the view
        super().__init__("nested", "no_title")

        # remove the title
        self.set_title()
