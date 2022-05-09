from sepal_ui import sepalwidgets as sw

from component.model import FARModel
from component.message import cm

from .fcc_view import *
from .var_view import *
from .compute_view import *


class ParameterTile(sw.Tile):
    def __init__(self, aoi_model):

        # gather the model
        self.far_model = FARModel()
        self.aoi_model = aoi_model

        # create the stepper header
        fcc_step = sw.StepperStep(
            key=1,
            step=1,
            complete=False,
            editable=True,
            children=[cm.param.fcc.stepper],
        )
        var_step = sw.StepperStep(
            key=2,
            step=2,
            complete=False,
            editable=True,
            children=[cm.param.var.stepper],
        )
        compute_step = sw.StepperStep(
            key=3,
            step=3,
            complete=False,
            editable=True,
            children=[cm.param.compute.stepper],
        )
        header = sw.StepperHeader(children=[fcc_step, var_step, compute_step])

        content = sw.StepperItems(
            children=[
                sw.StepperContent(
                    key=1, step=1, children=[FCCView(self.far_model, self.aoi_model)]
                ),
                sw.StepperContent(key=2, step=2, children=[VarView(self.far_model)]),
                sw.StepperContent(
                    key=3, step=3, children=[ComputeView(self.far_model)]
                ),
            ]
        )

        stepper = sw.Stepper(alt_labels=True, children=[header, content])

        # createt the tile
        super().__init__("parameter_tile", "Parameters", inputs=[stepper])
