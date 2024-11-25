from pydantic import BaseModel
from models import Artists
from storage import Buckets
from utills.encode_link import encode_link
from utills.path_manager import make_path


class ArtistShortInfo(BaseModel):
    Id: str | None = None
    Name: str | None = None
    ProfileImageUrl: str | None = None
    ContentType: str | None = None


def get_artist_short_info(
        artist: Artists
) -> ArtistShortInfo:
    data = ArtistShortInfo()
    data.Id = artist.Id
    data.Name = artist.Name
    data.ProfileImageUrl = encode_link(
        bucket_name=Buckets.USER_BUCKET_NAME,
        path=make_path(artist.DirectoryName, artist.ProfileImage, is_file=True)
    ) if artist.ProfileImage else None
    data.ContentType = artist.ContentType
    return data
