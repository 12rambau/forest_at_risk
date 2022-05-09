from sepal_ui import sepalwidgets as sw

from .fcc_view import *
from .var_view import *
from .compute_view import *


class ParameterTile(sw.Tile):
    def __init__(self, model, aoi_model):

        # gather the model
        self.model = model
        self.aoi_model = aoi_model

        # create the stepper header
        header = sw.StepperHeader(
            children=[
                sw.StepperStep(
                    key=1, step=1, complete=False, editable=True, children=["fcc"]
                ),
                sw.StepperStep(
                    key=2, step=2, complete=False, editable=True, children=["variables"]
                ),
                sw.StepperStep(
                    key=3, step=3, complete=False, editable=True, children=["compute"]
                ),
            ]
        )

        content = sw.StepperItems(
            children=[
                sw.StepperContent(key=1, step=1, children=[FCCView(model, aoi_model)]),
                sw.StepperContent(key=2, step=2, children=[VarView(model)]),
                sw.StepperContent(key=3, step=3, children=[ComputeView(model)]),
            ]
        )

        stepper = sw.Stepper(alt_labels=True, children=[header, content])

        # createt the tile
        super().__init__("parameter_tile", "Parameters", inputs=[stepper])
