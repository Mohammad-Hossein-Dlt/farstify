from typing import Annotated
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import InvalidTokenError
from pydantic import BaseModel
from starlette import status
from constants import AccountTypes

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

SECRET_KEY = '8def8f830990608125a82af8c56c0a787b8c794cacf3ee6cfc17ebe9f9597d20'
ALGORITHM = 'HS256'

tokenBearer = HTTPBearer()

op_tokenBearer = HTTPBearer(auto_error=False)


class TokenData(BaseModel):
    user_name: str | None = None
    user_id: int | None = None
    account_type: str | None = None
    permission: bool = False


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(encoded_token: str, empty_data: bool = False) -> TokenData:
    try:
        payload = jwt.decode(encoded_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("username")
        user_id: int = payload.get("id")
        account_type: str = payload.get("type")
        if user_name is None or user_id is None or account_type is None:
            if empty_data:
                return TokenData()
            else:
                raise credentials_exception
        return TokenData(user_name=user_name, user_id=user_id, account_type=account_type, permission=True)
    except InvalidTokenError:
        if empty_data:
            return TokenData()
        else:
            raise credentials_exception


def decode_artist_access_token(
        token: Annotated[HTTPAuthorizationCredentials, Depends(op_tokenBearer)],
) -> TokenData:
    if token:
        token_data = decode_access_token(encoded_token=token.credentials, empty_data=False)
        if token_data.account_type != AccountTypes.artist:
            raise HTTPException(403, "you are not artist")
        return token_data

    raise credentials_exception


def decode_user_access_token(
        token: Annotated[HTTPAuthorizationCredentials, Depends(op_tokenBearer)],
) -> TokenData:
    if token:
        token_data = decode_access_token(encoded_token=token.credentials, empty_data=False)
        if token_data.account_type != AccountTypes.user:
            raise HTTPException(403, "you are not user")
        return token_data

    raise credentials_exception


def optional_decode_user_access_token(
        token: Annotated[HTTPAuthorizationCredentials, Depends(op_tokenBearer)],
) -> TokenData:
    if token:
        token_data = decode_access_token(encoded_token=token.credentials, empty_data=True)
        return token_data
    else:
        return TokenData()


token_dependency = Annotated[TokenData, Depends(decode_access_token)]

artist_token_dependency = Annotated[TokenData, Depends(decode_artist_access_token)]

user_token_dependency = Annotated[TokenData, Depends(decode_user_access_token)]

optional_user_token_dependency = Annotated[TokenData, Depends(optional_decode_user_access_token)]

