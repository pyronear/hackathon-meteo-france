from dotenv import load_dotenv

load_dotenv()

import os

from src.pyrorisk.sources.fwi import main
from src.shared.libs.s3 import S3Bucket

S3 = S3Bucket(
    bucket_name="hackathon-meteo-france",
    endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    region_name=os.getenv("AWS_REGION_NAME"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


@click.command()
@click.option("--date", help="The date of the FWI image to download and process.")
def main(date):
    """
    Download and process the FWI image for the given date, and upload the results to S3.
    """
    print(f"Processing FWI image for date: {date}")
    json_fwi = main(date)
    print("Uploading results to S3...")
    S3.write_json_to_s3(json_fwi, f"output/fwi/{date}.json")
    print("Done!")


if __name__ == "__main__":
    main()
