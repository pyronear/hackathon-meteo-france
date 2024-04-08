import json
from io import BytesIO

import geopandas as gpd
import rasterio
import requests
from rasterio.features import shapes

from src.api.schemas.fwi import FWILoadInput

__all__ = ["load_fwi_data"]

BASE_URL = "https://ies-ows.jrc.ec.europa.eu/effis"

DEFAULT_ARGS = {
    "LAYERS": "mf010.fwi",
    "FORMAT": "image/tiff",
    "TRANSPARENT": "true",
    "SINGLETILE": "false",
    "SERVICE": "wms",
    "VERSION": "1.1.1",
    "REQUEST": "GetMap",
    "STYLES": "",
    "SRS": "EPSG:4326",
    "BBOX": "-5.0,43.0,10.0,52.0",
    "WIDTH": "1600",
    "HEIGHT": "1200",
    "TIME": "2021-07-01",
}


def load_fwi_data(input: FWILoadInput):
    return gpd_to_json(process(get_fwi_image(input.date)))


def get_fwi_image(date):
    args = DEFAULT_ARGS.copy()
    args["TIME"] = date
    url = BASE_URL + "?" + "&".join([f"{k}={v}" for k, v in args.items()])
    response = requests.get(url, stream=True)

    return response


def process(response):
    with rasterio.open(BytesIO(response.content)) as src:
        image = src.read(1)  # first band
        results = (
            {"properties": {"fwi_pixel_value": v}, "geometry": s}
            for i, (s, v) in enumerate(shapes(image, transform=src.meta["transform"]))
        )

        gpd_polygonized_raster = (
            gpd.GeoDataFrame.from_features(list(results), crs=src.meta["crs"])
            .query("fwi_pixel_value != 0")
            .assign(fwi_category=lambda x: x["fwi_pixel_value"].apply(_fwi_category))
        )

    return gpd_polygonized_raster


def _fwi_category(fwi_pixel_val: int) -> int:
    categories = [
        (58, 6),
        (145, 1),
        (192, 5),
        (210, 2),
        (231, 4),
    ]

    for threshold, risk_value in categories:
        if fwi_pixel_val <= threshold:
            return risk_value

    return 3


def gpd_to_json(geodataframe: gpd.GeoDataFrame):
    json_fwi = geodataframe.to_json()
    json_fwi = json.loads(json_fwi)
    for feature_dict in json_fwi["features"]:
        del feature_dict["id"]
    return {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"},
        },
        "features": json_fwi["features"],
    }
