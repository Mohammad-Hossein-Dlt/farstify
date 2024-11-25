import re
from fastapi import HTTPException
from db_dependency import db_dependency
from models import Users


async def uniq_user_name(
        db: db_dependency,
        user_name: str,
) -> bool:
    return True if db.query(Users).where(Users.UserName == user_name).count() == 0 else False


def check_username(username: str):
    check = bool(re.match(r"^[A-Za-z0-9_]+$", username))
    if check:
        return True
    else:
        raise HTTPException(403, "usernames can only use letters, numbers and underscores")
