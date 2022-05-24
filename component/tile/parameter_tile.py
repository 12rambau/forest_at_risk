from sepal_ui import sepalwidgets as sw

from component.model import FARModel
from component.message import cm
from component import widget as cw

from .fcc_view import *
from .var_view import *
from .advance_view import *


class ParameterTile(sw.Tile):
    def __init__(self, aoi_model):

        # gather the model
        self.far_model = FARModel()
        self.aoi_model = aoi_model

        # create the stepper header
        fcc_step = cw.StepperStep(1, cm.param.fcc.stepper)
        var_step = cw.StepperStep(2, cm.param.var.stepper)
        compute_step = cw.StepperStep(3, cm.param.advance.stepper)
        header = sw.StepperHeader(children=[fcc_step, var_step, compute_step])

        # set up the stepper content
        fcc_step = cw.StepperContent(1, FCCView(self.far_model, self.aoi_model))
        var_step = cw.StepperContent(2, VarView(self.far_model))
        compute_step = cw.StepperContent(3, AdvanceView(self.far_model, self.aoi_model))
        content = sw.StepperItems(children=[fcc_step, var_step, compute_step])

        stepper = sw.Stepper(alt_labels=True, children=[header, content])

        # createt the tile
        super().__init__("parameter_tile", cm.param.title, inputs=[stepper])
