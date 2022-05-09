from sepal_ui import sepalwidgets as sw

from component import parameter as cp
from component import scripts as cs


class FCCView(sw.Tile):
    """
    Tile to select the forest cover product
    retreive all the information from the GEE ?
    """

    def __init__(self, model, aoi_model):

        # gather the model
        self.model = model
        self.aoi_model = aoi_model

        # create the widget
        self.w_source = sw.Select(
            label="source of the forest cover change", items=cp.fcc_sources
        )
        self.w_from = sw.Select(
            label="from", no_data_text="select source first", items=[]
        )
        self.w_to = sw.Select(
            label="to", no_data_text="select a source first", items=[]
        )

        # create the view
        super().__init__(
            "nested",
            "no_title",
            inputs=[self.w_source, self.w_from, self.w_to],
            btn=sw.Btn("load forest change"),
            alert=sw.Alert(),
        )

        # remove the title and nest the tile
        self.nest()

    def on_click(self, widget, event, data):
        """load the fcc map according to the selected data"""

        pass

    def on_select(self, change):
        """sanity checks after selecting a new forest cover source"""

        # exist if nothing is selected
        if change["new"] is None:
            return

        # check if the AOI is set
        if self.aoi_model.name is None:
            raise Exception("no aoi is set")

        # check if the aoi is covered by this source
        if self.w_source.v_model == "TMF":
            is_tmf_covered
