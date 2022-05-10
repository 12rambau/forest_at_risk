import ee


def get_wdpa():

    protected_feature = ee.FeatureCollection("WCMC/WDPA/current/polygons")

    protected_image = (
        protected_feature.filter(ee.Filter.neq("WDPAID", {}))
        .reduceToImage(properties=["WDPAID"], reducer=ee.Reducer.first())
        .gt(0)
        .unmask(0)
        .rename("wdpa")
    )

    return protected_image
