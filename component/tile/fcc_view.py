from sepal_ui import sepalwidgets as sw
from sepal_ui.scripts import utils as su

from component import parameter as cp
from component import scripts as cs
from component.message import cm


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
        items = [
            {"text": getattr(cm.param.fcc.sources, s), "value": s}
            for s in cp.fcc_sources
        ]
        self.w_source = sw.Select(label=cm.param.fcc.widget.source.lbl, items=items)
        self.w_start = sw.Select(
            label=cm.param.fcc.widget.start.lbl,
            no_data_text=cm.param.fcc.error.no_data,
            items=[],
        )
        self.w_end = sw.Select(
            label=cm.param.fcc.widget.end.lbl,
            no_data_text=cm.param.fcc.error.no_data,
            items=[],
        )

        # make sure widget are unavailble before a aoi is selected
        self.widgets = [self.w_source, self.w_start, self.w_end]
        self._update_aoi(None)

        # link to the object
        (
            self.model.bind(self.w_source, "fcc_source")
            .bind(self.w_start, "fcc_start")
            .bind(self.w_end, "fcc_end")
        )

        # create the view
        super().__init__("nested", "", inputs=self.widgets)

        # remove the title and nest the tile
        self.nest()

        # add js behaviour
        self.aoi_model.observe(self._update_aoi, "name")
        self.w_source.observe(self.on_select, "v_model")

    def _update_aoi(self, change):
        """change the widget visibility according to aoi selection"""

        # check if an aoi is selected by checking the name (set automatically)
        name = self.aoi_model.name
        is_unset = name is None or name == "!!disabled!!"

        # apply it to every widget
        for i in self.widgets:
            i.v_model = None
            i.disabled = is_unset
            i.persistent_hint = is_unset
            i.hint = cm.param.fcc.error.no_aoi if is_unset else None

        return

    def on_click(self, widget, event, data):
        """load the fcc map according to the selected data"""

        pass

    @su.switch("loading", on_widgets=["w_source", "w_end", "w_start"])
    def on_select(self, change):
        """sanity checks after selecting a new forest cover source"""

        # remove any selected year
        self.w_start.v_model = None
        self.w_end.v_model = None

        # exist if nothing is selected
        if self.w_source.v_model is None:
            return

        # check if the aoi is covered by this source
        source = self.w_source.v_model
        if source == "TMF":
            if not cs.is_tmf_covered(self.aoi_model.feature_collection):
                self.w_source.error_messages = [cm.param.fcc.error.not_covered]

        # in any cases change the item list
        # based on the date range of the dataset
        items = [
            y
            for y in range(
                cp.fcc_sources[source]["end"], cp.fcc_sources[source]["start"], -1
            )
        ]
        self.w_end.items = self.w_start.items = items

        return
