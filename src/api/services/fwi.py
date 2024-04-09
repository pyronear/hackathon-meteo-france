import json
import os

from src.api.schemas.fwi import FWILoadInput
from src.shared.file_utils import get_project_data_folder_dir
from src.shared.libs.s3 import S3Bucket

__all__ = ["load_fwi_data"]


def load_fwi_data(input: FWILoadInput):
    year, month, day = input.date.split("-")

    file_path = get_project_data_folder_dir() / "raw/test.json"

    S3 = S3Bucket(
        bucket_name="hackathon-meteo-france",
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
        region_name=os.getenv("AWS_REGION_NAME"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    S3.download_file(
        object_key=f"fwi/year={year}/month={month}/day={day}/fwi_values.json",
        file_path=file_path,
    )

    with open(file_path, "r") as f:
        fwi_data = json.load(f)

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

    for el in fwi_data["features"]:
        el["properties"]["fwi_category"] = _fwi_category(
            el["properties"]["fwi_pixel_value"]
        )

    return fwi_data
