import os
import boto3
import json

from botocore.client import Config

def get_minio_client(): 
    endpoint_url = os.environ["MINIO_ENDPOINT_URL"]
    return boto3.client(
        "s3",
        endpoint_url=f"http://{endpoint_url}",
        aws_access_key_id=os.environ["MINIO_ROOT_USER"],
        aws_secret_access_key=os.environ["MINIO_ROOT_PASSWORD"],
        config=Config(signature_version="s3v4"),
        region_name="us-east-1"
    )

def read_json(client, bucket: str, key: str):
    obj = client.get_object(Bucket=bucket, Key=key)
    return json.loads(obj["Body"].read())

def read_bytes(client, bucket: str, key: str):
    obj = client.get_object(Bucket=bucket, Key=key)
    return obj["Body"].read()