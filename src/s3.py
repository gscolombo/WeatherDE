from typing import Any
import boto3


class S3Client():
    client: Any

    def __init__(self):
        self.client = boto3.resource('s3')

    def get_buckets(self):
        return self.client.buckets.all()

    def put_object(self, bucket_name: str, filename: str, data: dict):
        self.client \
            .Bucket(bucket_name) \
            .put_object(Key=filename, Body=data)
