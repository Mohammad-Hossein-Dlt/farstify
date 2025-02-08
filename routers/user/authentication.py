import models
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from access_token import create_access_token
from storage import storage, Buckets
from db_dependency import db_dependency
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from actions.response_model import ResponseMessage
from typing import Annotated
from sqlalchemy import and_, or_
from utills.path_manager import make_path
from constants import AccountTypes

router = APIRouter(prefix="/user/authentication", tags=["User-Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SignUp(BaseModel):
    Name: str
    Phone: str
    Password: str
    Email: str | None = None
    VerifyCode: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/sign_up", status_code=status.HTTP_201_CREATED)
async def sign_up_action(
        db: db_dependency,
        sign_up: SignUp,
):
    check = db.query(
        models.Users
    ).where(
        models.Users.Phone == sign_up.Phone
    ).first()

    verify_code = db.query(
        models.UsersTemp
    ).where(
        and_(
            models.UsersTemp.Phone == sign_up.Phone,
            models.UsersTemp.VerifyCode == sign_up.VerifyCode
        )
    ).first()

    verify_code = True

    if check:
        raise HTTPException(201, "general already signed up!")

    if verify_code is None:
        raise HTTPException(403, "you are not verified")

    user = models.Users()
    user.Name = sign_up.Name.strip()
    user.Phone = sign_up.Phone.strip()
    user.Password = pwd_context.hash(sign_up.Password.strip())
    user.Email = sign_up.Email.strip() if sign_up.Email else None
    db.add(user)

    db.commit()

    path = make_path(user.DirectoryName, is_file=False)
    storage.put_object(Bucket=Buckets.USER_BUCKET_NAME, Key=path)

    return ResponseMessage(error=False, message="User has been signed up!")


@router.post("/sign_in", status_code=status.HTTP_201_CREATED)
async def sign_in(
        db: db_dependency,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    check = db.query(
        models.Users
    ).where(
        or_(
            models.Users.Phone == form_data.username,
            models.Users.UserName == form_data.username,
        )
    ).first()

    verify_code = db.query(
        models.UsersTemp
    ).where(
        and_(
            models.UsersTemp.Phone == form_data.username,
        )

    ).first()

    if check is None:
        raise HTTPException(403, "You are not signed up")

    password_check = pwd_context.verify(form_data.password, check.Password)

    verify_code_check = verify_code.VerifyCode == form_data.password if verify_code else False

    if password_check or verify_code_check:
        to_encode = {"username": check.UserName, "id": check.Id, "type": AccountTypes.user}
        access_token = create_access_token(to_encode)
        return Token(access_token=access_token, token_type="bearer")

    if not password_check or not verify_code:
        raise HTTPException(403, "Incorrect password or verified")
