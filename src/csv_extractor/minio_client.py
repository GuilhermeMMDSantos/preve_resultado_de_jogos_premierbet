import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import os
import logging
import io

logger = logging.getLogger(__name__)
def get_minio_client():
    endpoint_url = os.environ["MINIO_ENDPOINT"]
    return boto3.client(
        "s3",
        endpoint_url=f"http://{endpoint_url}",
        aws_access_key_id=os.environ["MINIO_ROOT_USER"],
        aws_secret_access_key=os.environ["MINIO_ROOT_PASSWORD"],
        config=Config(signature_version="s3v4"),
        region_name="us-east-1"
    )

def ensure_bucket_exists(minio_client, bucket:str):
    try:
        minio_client.head_bucket(Bucket=bucket)
    except ClientError:
        logger.info("Bucket %s não existe, criando...")
        minio_client.create_bucket(Bucket=bucket)

def upload_csv(minio_client, bucket:str, key:str, payload: bytes):
    minio_client.put_object(Bucket=bucket, Key=key, Body=io.BytesIO(payload), ContentType="application/json")
    logger.info("Gravado s3://%s/%s (%d bytes) ", bucket, key, len(payload))