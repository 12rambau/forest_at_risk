from sepal_ui import model
from traitlets import Unicode, Int


class FARModel(model.Model):

    # inputs
    fcc_source = Unicode(None, True).tag(sync=True)
    "the source of the fcc layer"

    fcc_start = Int(None, True).tag(sync=True)
    "the starting date of the fcc layer"

    fcc_end = Int(None, True).tag(sync=True)
    "the end year of the fcc layer"

    pass
