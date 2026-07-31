import logging
import boto3
import os
import json
import io

from botocore.client import Config
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)

def get_minio_client():
    minio_endpoint = os.environ["MINIO_ENDPOINT"]
    return boto3.client(
        "s3",
        endpoint_url = f"http://{minio_endpoint}",
        aws_access_key_id = os.environ["MINIO_ROOT_USER"],
        aws_secret_access_key = os.environ["MINIO_ROOT_PASSWORD"],
        config=Config(signature_version="s3v4"),
        region_name="us-east-1"
    )


def ensure_bucket_exist(client, bucket: str):
    try:
        client.head_bucket(Bucket=bucket)
    except ClientError:
        logger.info("bucket '%s' nao existe. criando...", bucket)
        client.create_bucket(Bucket=bucket)

def upload_json(client, bucket:str, key:str, payload:dict):
    body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    client.put_object(Bucket=bucket, Key=key, Body=io.BytesIO(body), ContentType="application/json")
    logger.info("Gravado s3://%s/%s (%d bytes) ", bucket, key, len(body))