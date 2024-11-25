import base64

from fastapi import HTTPException
import jwt
from jwt import InvalidTokenError
from pydantic import BaseModel

SECRET_KEY = '8def8f830990608125a82af8c56c0a787b8c794cacf3ee6cfc17ebe9f9597d20'
ALGORITHM = 'HS256'


class UrlData(BaseModel):
    bucket: str | None = None
    path: str | None = None


def encode_link(bucket_name: str, path: str):
    to_encode = {
        "bucket": bucket_name,
        "path": path
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_link(token: str) -> UrlData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        bucket: str = payload.get("bucket")
        path: int = payload.get("path")
        if bucket is None or path is None:
            return UrlData()
        return UrlData(bucket=bucket, path=path)
    except InvalidTokenError:
        return UrlData()
