import boto3


class Buckets:
    DOCUMENT_BUCKET_NAME = "farstify"
    USER_BUCKET_NAME = "farstify-users"
    CHUNKS_BUCKET_NAME = "farstify-chunks"


STORAGE_ENDPOINT = "https://storage.iran.liara.space"
ACCESS_KEY = "8od7lamm3eqhhs80"
SECRET_KEY = "1a9991df-4428-4242-b24e-1c01a3fd3231"

storage = boto3.client(
    "s3",
    endpoint_url=STORAGE_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

resources = boto3.resource(
    "s3",
    endpoint_url=STORAGE_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)


def get_bucket(BUCKET_NAME: str):
    return resources.Bucket(BUCKET_NAME)


def storage_delete_folder(path: str, bucket_name: str):
    get_bucket(bucket_name).objects.filter(Prefix=path).delete()


def storage_delete_file(path: str, bucket_name: str):
    try:
        storage.head_object(Bucket=bucket_name, Key=path)
        storage.delete_object(Bucket=bucket_name, Key=path)
        return True
    except Exception as ex:
        return False
