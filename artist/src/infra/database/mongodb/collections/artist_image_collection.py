from src.domain.schemas.artist.artist_image import ArtistImageModel
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone


class ArtistImageCollection(ArtistImageModel, Document):

    id: PydanticObjectId = None
    artist_id: PydanticObjectId
    cover: str
    is_main: bool = False
    order: int | None = None
    
    class Settings:
        name = "ArtistImage"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
