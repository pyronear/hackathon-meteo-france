import json
import os

import ast

import pandas as pd
import pandas_geojson as pdg

from src.api.schemas.wildfires import WildfiresLoadInput
from src.shared.file_utils import get_project_data_folder_dir
from src.shared.libs.s3 import S3Bucket

__all__ = ["load_wildfires_data"]


def load_wildfires_data(input: WildfiresLoadInput):
    file_path = get_project_data_folder_dir() / "raw/wildfires.csv"

    S3 = S3Bucket(
        bucket_name="hackathon-meteo-france",
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
        region_name=os.getenv("AWS_REGION_NAME"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    S3.download_file(
        object_key="wildfires/firepoints.csv",
        file_path=file_path,
    )

    data = pd.read_csv(file_path)

    geojson = pdg.GeoJSON.from_dataframe(
        data.query(f"acq_date == '{input.date}'"),
        geometry_type_col="type",
        coordinate_col="coordinates",
        property_col_list=["confidence"],
    )


    # TODO: fix this properly, this is a hack to convert the string coordinates to a list
    geojsonFire =  geojson.to_dict()

    geojsonfire_features_fixed = [{**feature, "geometry": {**feature['geometry'], "coordinates": ast.literal_eval(feature['geometry']['coordinates'])}} for feature in geojsonFire['features']]
    geojsonFire['features'] = geojsonfire_features_fixed

    return geojsonFire
