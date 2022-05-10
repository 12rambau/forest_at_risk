from itertools import product

from shapely import geometry as sg
from pyproj import CRS, Transformer
import numpy as np
import geopandas as gpd

from component import parameter as cp


def generate_grid(aoi_model):
    """
    generate an ee.FeatureCollection to download the datas

    Args:
        aoi (sw.AoiModel): the model of the AOI

    Returns:
        (gdf): the grid
    """

    # check if the aoi have already been grided
    raw_dir = cp.down_dir / aoi_model.name / "raw"
    raw_dir.mkdir(exist_ok=True, parents=True)

    path = raw_dir / f"{aoi_model.name}_grid.geojson"
    if path.is_file():
        return gpd.read_file(path)

    # get the shape of the aoi in EPSG:4326 proj
    aoi_gdf = aoi_model.gdf.to_crs("EPSG:3857")

    # retreive the bounding box
    aoi_bb = sg.box(*aoi_gdf.total_bounds)
    aoi_bb.bounds

    # compute the longitude and latitude in the apropriate CRS
    crs_4326 = CRS.from_epsg(4326)
    crs_3857 = CRS.from_epsg(3857)
    crs_min_x, crs_min_y, crs_max_x, crs_max_y = crs_3857.area_of_use.bounds

    proj = Transformer.from_crs(4326, 3857, always_xy=True)
    bl = proj.transform(crs_min_x, crs_min_y)
    tr = proj.transform(crs_max_x, crs_max_y)

    # the planet grid is constructing a 2048x2048 grid of SQUARES.
    # The latitude extends is bigger (20048966.10m VS 20026376.39) so to ensure the "squariness"
    # Planet lab have based the numerotation and extends of it square grid on the longitude only.
    # the extreme -90 and +90 band it thus exlucded but there are no forest there so we don't care
    longitudes = np.linspace(bl[0], tr[0], 2048 + 1)

    # the planet grid size cut the world in 248 squares vertically and horizontally
    box_size = (tr[0] - bl[0]) / 2048

    # filter with the geometry bounds
    min_lon, min_lat, max_lon, max_lat = aoi_gdf.total_bounds

    # filter lon and lat
    lon_filter = longitudes[
        (longitudes > (min_lon - box_size)) & (longitudes < max_lon + box_size)
    ]
    lat_filter = longitudes[
        (longitudes > (min_lat - box_size)) & (longitudes < max_lat + box_size)
    ]

    # get the index offset
    x_offset = np.nonzero(longitudes == lon_filter[0])[0][0]
    y_offset = np.nonzero(longitudes == lat_filter[0])[0][0]

    # create the grid
    x, y, names, squares = [], [], [], []
    for ix, iy in product(range(len(lon_filter) - 1), range(len(lat_filter) - 1)):

        # fill the grid values
        x.append(ix + x_offset)
        y.append(iy + y_offset)
        names.append(f"{x[-1]:4d}E-{y[-1]:4d}N")
        box = sg.box(
            lon_filter[ix], lat_filter[iy], lon_filter[ix + 1], lat_filter[iy + 1]
        )
        squares.append(box)

    # create a buffer grid in lat-long
    data = {"x": x, "y": y, "names": names, "geometry": squares}
    grid = gpd.GeoDataFrame(data, crs="EPSG:3857")

    # cut the grid to the aoi extends
    mask = grid.intersects(aoi_gdf.dissolve()["geometry"][0])
    grid = grid.loc[mask]

    # project back to 4326
    grid = grid.to_crs("EPSG:4326")

    # export the grid as a json file
    grid.to_file(path, driver="GeoJSON")

    # debug print the grid size
    print(len(grid))

    return grid
