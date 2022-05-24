from sepal_ui import sepalwidgets as sw
from sepal_ui.scripts import utils as su

from component.message import cm
from component import scripts as cs


class AdvanceView(sw.Tile):
    def __init__(self, model, aoi_model):

        # gather the model
        self.model = model
        self.aoi_model = aoi_model

        # add advanced parameters

        # sampling
        sampling_title = sw.Html(tag="h3", chldren=["sampling"])
        size = sw.NumberField(
            label="number of samples", v_model=10000, max=10e6, readonly=False
        )
        csize = sw.NumberField(label="csize", v_model=10, max=100, readonly=False)

        # model
        model_title = sw.Html(tag="h3", children=["Model"])
        bet_start = sw.Select(
            items=[{"text": "Simple GLM estimates", "value": -99}],
            v_model=-99,
            label="beta start",
        )
        priorVrho = sw.Select(
            items=[{"text": "1/Gamma", "value": -1}], v_model=-1, label="priorVrho"
        )
        mcmc = sw.NumberField(label="mcmc", v_model=1000, max=10000, readonly=False)
        thin = sw.NumberField(label="thin", v_model=1, readonly=False)

        # create the view
        super().__init__(
            "nested",
            "no_title",
            inputs=[
                sampling_title,
                sampling_title,
                size,
                csize,
                model_title,
                bet_start,
                priorVrho,
                mcmc,
                thin,
            ],
        )

        # remove the title
        # self.nest()
