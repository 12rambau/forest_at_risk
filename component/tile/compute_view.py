from sepal_ui import sepalwidgets as sw
from sepal_ui.scripts import utils as su

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

    @su.loading_button(debug=True)
    def compute_far(self, widget, event, data):

        # create the feature collection grid
        grid = cs.generate_grid(self.aoi_model)
        total = len(grid)

        # aggregate all the images to download
        image_dict = {}
        image_dict["fcc23"] = cs.get_fcc(
            self.model.fcc_source, self.model.fcc_start, self.model.fcc_end
        )
        image_dict["elevation"] = cs.get_elevation()
        image_dict["slope"] = cs.get_slope()
        image_dict["wdpa"] = cs.get_wdpa()

        # download all the images to the raw folder
        for name, image in image_dict.items():
            cs.download_image(
                image=image,
                grid=grid,
                aoi_name=self.aoi_model.name,
                layer=name,
                alert=self.alert,
            )

        self.alert.add_msg("download complete")

        # compute stuff

        # display them on the map

        return
