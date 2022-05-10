from urllib.request import urlretrieve
import zipfile

from osgeo import gdal
import ee

from component import parameter as cp

ee.Initialize()


def download_image(image, grid, aoi_name, layer, alert):
    """download an image from GEE to appropriate folder using a grid"""

    # check if the vrt already exist
    vrt = cp.down_dir / aoi_name / f"{layer}.vrt"

    if vrt.is_file():
        return

    # loop in the grid
    total = len(grid)
    dst_list = []
    for i, grid_cell in grid.iterrows():

        # name the file
        # names in the grid cell as name is a protected geoseries index
        description = f"{layer}_{grid_cell.names}"
        folder = cp.down_dir / aoi_name / "raw"
        folder.mkdir(exist_ok=True)
        dst_list.append(folder / f"{description}.tif")

        if not dst_list[i].is_file():

            # create the download order
            name = f"{description}_zipimage"
            link = image.getDownloadURL(
                {
                    "name": layer,
                    "region": ee.Geometry(grid_cell.geometry.__geo_interface__),
                    "filePerBand": False,
                    "scale": 30,
                }
            )

            # extract information from the tmp zip file
            tmp = folder / f"{name}.zip"
            urlretrieve(link, tmp)

            with zipfile.ZipFile(tmp, "r") as zip_:
                data = zip_.read(zip_.namelist()[0])
                dst_list[i].write_bytes(data)
            tmp.unlink()

        alert.update_progress((i + 1) / total, f"downloading {layer}:")

    # build the vrt
    filepaths = [str(dst) for dst in dst_list]
    ds = gdal.BuildVRT(str(vrt), filepaths)
    ds.FlushCache()

    # check that the file was effectively created (gdal doesn't raise errors)
    if not vrt.is_file():
        raise Exception(f"the vrt {vrt} was not created")

    return


def geojson_to_ee(geo_json, geodesic=False, encoding="utf-8"):
    """
    Transform a geojson object into a featureCollection
    No sanity check is performed on the initial geo_json. It must respect the
    `__geo_interface__ <https://gist.github.com/sgillies/2217756>`__.

    Args:
        geo_json (dict): a geo_json dictionnary
        geodesic (bool, optional): Whether line segments should be interpreted as spherical geodesics. If false, indicates that line segments should be interpreted as planar lines in the specified CRS. If absent, defaults to True if the CRS is geographic (including the default EPSG:4326), or to False if the CRS is projected. Defaults to False.
        encoding (str, optional): The encoding of characters. Defaults to "utf-8".

    Returns:
        (ee.FeatureCollection): the created featurecollection
    """

    # from a featureCollection
    if geo_json["type"] == "FeatureCollection":
        for feature in geo_json["features"]:
            if feature["geometry"]["type"] != "Point":
                feature["geometry"]["geodesic"] = geodesic
        features = ee.FeatureCollection(geo_json)
        return features

    # from a single feature
    elif geo_json["type"] == "Feature":
        geom = None
        # Checks whether it is a point
        if geo_json["geometry"]["type"] == "Point":
            coordinates = geo_json["geometry"]["coordinates"]
            longitude = coordinates[0]
            latitude = coordinates[1]
            geom = ee.Geometry.Point(longitude, latitude)
        # for every other geometry simply create a geometry
        else:
            geom = ee.Geometry(geo_json["geometry"], "", geodesic)

        return geom

    # some error handling because we are fancy
    else:
        raise Exception("Could not convert the geojson to ee.Geometry()")

    return
