from sepal_ui import sepalwidgets as sw


class ParameterTile(sw.Tile):
    def __init__(self, model):

        # gather the model
        self.model = model

        super().__init__("parameter_tile", "Parameters")
