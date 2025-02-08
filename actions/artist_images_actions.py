from pydantic import BaseModel
from models import Artists, ArtistImages
from utills.path_manager import make_path
from utills.encode_link import encode_link
from storage import Buckets


class ArtistImageInfo(BaseModel):
    Id: int | None = None
    Url: str | None = None
    Order: str | None = None


def get_artist_image_info(
        artist: Artists,
        image: ArtistImages,
) -> ArtistImageInfo:
    data = ArtistImageInfo()

    data.Id = image.Id
    data.Url = encode_link(
        bucket_name=Buckets.USER_BUCKET_NAME,
        path=make_path(artist.DirectoryName, image.Image, is_file=True)
    )
    data.Order = image.OrderBy

    return data

