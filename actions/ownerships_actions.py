from pydantic import BaseModel
from actions.raw_artist_info_actions import RawArtistInfo, get_raw_artist_info
from db_dependency import db_dependency
import models


class OwnershipInfo(BaseModel):
    Id: int | None = None
    Artist: RawArtistInfo | None = None
    Order: int | None = None


def get_ownership_info(
        db: db_dependency,
        ownership: models.DocumentsOwners,
        artist: models.Artists | None = None,
) -> OwnershipInfo:
    data = OwnershipInfo()

    if not artist:
        artist = db.query(
            models.Artists
        ).where(
            models.Artists.Id == ownership.ArtistId,
        ).first()

    data.Id = ownership.Id
    data.Artist = get_raw_artist_info(artist)
    data.Order = ownership.OrderBy

    return data
