import models
import uuid
import pathlib
from passlib.context import CryptContext
from access_token import user_token_dependency, token_dependency
from actions.user_actions import user_profile_data
from storage import storage, Buckets, storage_delete_file
from db_dependency import db_dependency
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from actions.response_model import ResponseMessage
from sqlalchemy import and_
from utills.path_manager import make_path
from utills.check_username import uniq_user_name, check_username

router = APIRouter(prefix="/user/profile", tags=["User-Profile"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/profile", status_code=status.HTTP_201_CREATED)
async def verify_user(
        db: db_dependency,
        access_token: token_dependency,
):
    user = db.query(
        models.Users
    ).where(
        models.Users.UserName == access_token.user_name
    ).first()

    if not user:
        raise HTTPException(404, "an error occurred!")

    return user_profile_data(user)


@router.post("/change_profile_image", status_code=status.HTTP_201_CREATED)
async def change_profile_image(
        db: db_dependency,
        access_token: user_token_dependency,
        image_file: UploadFile = File(None),
        delete_image: bool = False,
):
    user = db.query(
        models.Users
    ).where(
        models.Users.Id == access_token.user_id
    ).first()

    main_path = make_path(user.DirectoryName, is_file=False)

    def delete_image_action(image: str):
        try:
            delete_previous = make_path(main_path, image, is_file=True)
            storage_delete_file(delete_previous, Buckets.USER_BUCKET_NAME)
        except Exception as ex:
            print(ex)

    if image_file and not delete_image:
        file_name = uuid.uuid4().hex + pathlib.Path(image_file.filename).suffix
        image_path = make_path(main_path, file_name, is_file=True)
        try:
            storage.upload_fileobj(image_file.file, Bucket=Buckets.USER_BUCKET_NAME, Key=image_path)
        except Exception as ex:
            print(ex)
        else:
            delete_image_action(user.ProfileImage)
            user.ProfileImage = file_name
            db.commit()
    elif not image_file and delete_image:
        delete_image_action(user.ProfileImage)
        user.ProfileImage = None
        db.commit()

    return ResponseMessage(error=False, message="User profile image has been changed!")


@router.put("/edit_profile", status_code=status.HTTP_201_CREATED)
async def edit_profile(
        db: db_dependency,
        access_token: user_token_dependency,
        name: str | None = None,
        email: str | None = None,
):
    user = db.query(
        models.Users
    ).where(
        models.Users.Id == access_token.user_id
    ).first()

    user.Name = name.strip() if name else user.Name
    user.Email = email.strip() if email else user.Email

    db.commit()
    return ResponseMessage(error=False, message="User profile has been changed!")


@router.put("/change_username", status_code=status.HTTP_201_CREATED)
async def change_username(
        db: db_dependency,
        access_token: user_token_dependency,
        username: str,
):
    username = username.strip()

    user = db.query(
        models.Users
    ).where(
        models.Users.Id == access_token.user_id
    ).first()

    if user and check_username(username=username):
        if await uniq_user_name(db, username):
            user.UserName = username
            db.commit()
            return ResponseMessage(error=False, message="User-name has been changed!")
        else:
            raise HTTPException(403, f"the username {username} is not available")


@router.put("/change_password", status_code=status.HTTP_201_CREATED)
async def change_password(
        db: db_dependency,
        access_token: user_token_dependency,
        password: str,
        newpassword: str,
):
    user = db.query(
        models.Users
    ).where(
        models.Users.Id == access_token.user_id
    ).first()

    if user is None:
        raise HTTPException(403, "You are not signed up")

    verify_code = db.query(
        models.UsersTemp
    ).where(
        and_(
            models.UsersTemp.Phone == user.Phone,
            models.UsersTemp.VerifyCode == password
        )

    ).first()

    if user and (pwd_context.verify(password, user.Password) or verify_code):
        user.Password = pwd_context.hash(newpassword.strip())
        db.commit()
        return ResponseMessage(error=False, message="User password has been changed!")
    elif user is None:
        raise HTTPException(403, "You are not signed up")
    elif user and not pwd_context.verify(password, user.Password):
        raise HTTPException(403, "Incorrect password")
    elif verify_code is None:
        raise HTTPException(403, "You are not verified")


@router.put("/change_phone", status_code=status.HTTP_201_CREATED)
async def change_phone(
        db: db_dependency,
        access_token: user_token_dependency,
        new_phone: str,
        verifycode: str,
):
    new_phone = new_phone.strip()

    new_phone_exists = db.query(
        models.Users
    ).where(
        models.Users.Phone == new_phone
    ).first()

    user = db.query(
        models.Users
    ).where(
        models.Users.Id == access_token.user_id
    ).first()

    if not user:
        raise HTTPException(403, "You are not signed up")

    verify_code = db.query(
        models.UsersTemp
    ).where(
        and_(
            models.UsersTemp.Phone == new_phone,
            models.UsersTemp.VerifyCode == verifycode
        )
    ).first()

    if new_phone_exists is None and verify_code:
        user.Phone = new_phone
        db.commit()
        return ResponseMessage(error=False, message="User phone has been changed!")
    elif new_phone_exists:
        raise HTTPException(403, "Your new phone already exists")
    elif not verify_code:
        raise HTTPException(403, "Your new phone not verified")
