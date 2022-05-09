import ee

from component import parameter as cp


def is_tmf_covered(geometry):
    """return true if there is more than 0 images"""

    return (
        ee.ImageCollection(cp.fcc_sources["TMF"]["asset"])
        .filterBounds(geometry)
        .size()
        .getInfo()
        != 0
    )


def get_fcc(source, start, end):
    """retreive the image from GEE based on the selected parameters"""

    if source == "TMF":

        # JRC annual product (AP)
        ap = ee.ImageCollection(cp.fcc_sources[source]["asset"]).mosaic().byte()

        # ap_allYear: forest if Y = 1 or 2.
        ap_forest = ap.where(ap.eq(2), 1)
        ap_all_year = ap_forest.where(ap_forest.neq(1), 0)

        # convert the dates in band number
        b_final = 2022 - 1990
        b_start = start - 1990
        b_end = end - 1990

        # Forest in start date
        ap_start = ap_all_year.select(list(range(b_start, b_final)))
        forest_start = ap_start.reduce(ee.Reducer.sum()).gte(1)

        # Forest in end date
        ap_end = ap_all_year.select(list(range(b_end, b_final)))
        forest_end = ap_end.reduce(ee.Reducer.sum()).gte(1)

        # Forest raster with 2 bands
        forest = forest_start.addBands(forest_end)
        forest = forest.select([0, 1], ["forest_start", "forest_end"])
        forest = forest.set("system:bandNames", ["forest_start", "forest_end"])

    elif source == "GFC":

        # we define a treecover at
        perc = 10

        # Hansen map
        gfc = ee.Image(cp.fcc_sources[source]["asset"])

        # Tree cover, loss, and gain
        treecover = gfc.select(["treecover2000"])
        lossyear = gfc.select(["lossyear"])

        # Forest in 2000
        forest2000 = treecover.gte(10)
        forest2000 = forest2000.toByte()

        # convert date in deforestation values
        v_start = start - 2000
        v_end = end - 2000

        # Deforestation
        loss_start = lossyear.gte(1).And(lossyear.lte(v_start))
        loss_end = lossyear.get(1).And(lossyear.lte(v_end))

        # Forest
        forest_start = forest2000.where(loss_start.eq(1), 0)
        forest_end = forest2000.where(loss_end.eq(1), 0)

        # Forest raster with 2 bands
        forest = forest_start.addBands(forest_end)
        forest = forest.select([0, 1], ["forest_start", "forest_end"])
        forest = forest.set("system:bandNames", ["forest_start", "forest_end"])

    return forest
