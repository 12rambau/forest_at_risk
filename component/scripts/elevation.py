import ee


def get_elevation():

    return ee.Image("CGIAR/SRTM90_V4").select("elevation")


def get_slope():

    return ee.Terrain.slope(ee.Image("CGIAR/SRTM90_V4").select("elevation"))
