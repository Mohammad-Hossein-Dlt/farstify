from pydantic import BaseModel
import models
from utills.encode_link import encode_link
from storage import Buckets
from utills.path_manager import make_path


class SingleUserProfileData(BaseModel):
    UserName: str | None = None
    Name: str | None = None
    ProfileImageUrl: str | None = None


def user_profile_data(user: models.Users) -> SingleUserProfileData:
    data = SingleUserProfileData()
    data.UserName = user.UserName
    data.Name = user.Name
    data.ProfileImageUrl = encode_link(
        bucket_name=Buckets.USER_BUCKET_NAME,
        path=make_path(user.DirectoryName, user.ProfileImage, is_file=True),
    ) if user.ProfileImage else None

    return data
