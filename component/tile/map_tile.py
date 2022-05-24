from sepal_ui import sepalwidgets as sw
from sepal_ui import mapping as sm
from sepal_ui.scripts import utils as su

from component import scripts as cs


class MapTile(sw.Tile):
    def __init__(self, aoi_model, model):

        # gather the models
        self.aoi_model = aoi_model
        self.model = model

        # create a map
        self.map = sm.SepalMap()

        # init the tile
        super().__init__(
            "map_tile",
            "Map",
            inputs=[self.map],
            btn=sw.Btn("compute forest at risk"),
            alert=sw.Alert(),
        )

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
