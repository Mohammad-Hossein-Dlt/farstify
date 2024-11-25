from pydantic import BaseModel
from models import Artists, ArtistImages
from utills.path_manager import make_path
from utills.encode_link import encode_link
from storage import Buckets


class ImageViewModel(BaseModel):
    id: int | None = None
    file: str | None = None
    url: str | None = None
    order: str | None = None


def artist_image_view_model(
        artist: Artists,
        image: ArtistImages,
) -> ImageViewModel:
    data = ImageViewModel()

    data.id = image.Id
    data.file = image.Image
    data.url = encode_link(
        bucket_name=Buckets.USER_BUCKET_NAME,
        path=make_path(artist.DirectoryName, image.Image, is_file=True)
    )
    data.order = image.OrderBy

    return data

