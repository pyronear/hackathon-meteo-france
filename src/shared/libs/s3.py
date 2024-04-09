import json

import boto3

__all__ = ["S3Bucket"]


class S3Bucket:

    def __init__(
        self,
        bucket_name: str,
        endpoint_url: str,
        region_name: str,
        aws_access_key_id: str,
        aws_secret_key: str,
    ) -> None:
        session_args = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_key,
            "region_name": region_name,
        }
        self.session = boto3.Session(**session_args)
        self.s3 = self.session.resource("s3", endpoint_url=endpoint_url)
        self.bucket = self.s3.Bucket(bucket_name)
        self.bucket_name = bucket_name

    def upload_file(self, file_path: str, object_key: str) -> None:
        """
        Uploads a file to the S3 bucket.

        Args:
            file_path (str): The local path of the file to upload.
            object_key (str): The S3 key (path) where the file will be stored.
        """
        self.bucket.upload_file(file_path, object_key)

    def write_json_to_s3(self, json_data: json, object_key: str) -> None:
        """
        Writes a JSON file on the S3 bucket.

        Args:
            json_data (json): The JSON data we want to upload.
            object_key (str): The S3 key (path) where the file will be stored.
        """
        self.bucket.put_object(
            Key=object_key, Body=bytes(json.dumps(json_data).encode("UTF-8"))
        )

    def download_file(self, object_key: str, file_path: str) -> None:
        """
        Downloads a file from the S3 bucket.

        Args:
            object_key (str): The S3 key (path) of the file to download.
            file_path (str): The local path where the file will be saved.
        """
        self.bucket.download_file(object_key, file_path)

    def list_files(
        self,
        patterns: list[str] = None,
        prefix: str = "",
        delimiter: str = "",
        limit: int = 0,
    ) -> list[str]:
        """
        Lists files in the S3 bucket.

        Args:
            patterns (list[str], optional): Only files with keys containing one of the patterns will be listed.
            prefix (str, optional): Only folders with keys starting with this prefix will be listed.
            delimiter (str, optional): The delimiter to use for the folder listing.
            limit (int, optional): Limit the number of files in the output list of the function.

        Returns:
            A list of file keys (paths) in the bucket.
        """
        files = []
        object_filter = self.bucket.objects.filter(Prefix=prefix, Delimiter=delimiter)
        if limit != 0:
            object_filter = object_filter.limit(limit)
        for obj in object_filter:
            if not patterns or (
                type(patterns) == list and any([p in obj.key for p in patterns])
            ):
                files.append(obj.key)
        return files
