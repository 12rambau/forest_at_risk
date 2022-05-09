from sepal_ui import sepalwidgets as sw

from component.message import cm
from component import scripts as cs


class ComputeView(sw.Tile):
    def __init__(self, model, aoi_model):

        # gather the model
        self.model = model
        self.aoi_model = aoi_model

        # create the view
        super().__init__(
            "nested", "no_title", btn=sw.Btn(cm.param.compute.btn), alert=sw.Alert()
        )

        # remove the title
        self.set_title()

        # add js behaviours
        self.btn.on_event("click", self.compute_far)

    def compute_far(self, widget, event, data):

        # create the feature collection grid
        grid = cs.generate_grid(self.aoi_model)

        # download the raw images

        # compute stuff

        # display them on the map

        return
