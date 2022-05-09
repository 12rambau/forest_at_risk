import ee

from component import parameter as cp


def is_tmf_covered(geometry):
    """return true if there is more than 0 images"""

    return (
        ee.ImageCollection(cp.gee_asset_id["TMF"])
        .filterBounds(geometry)
        .size()
        .getInfo()
        != 0
    )
