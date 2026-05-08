from src.domain.schemas.artist.artist_link import ArtistLinkModel
from src.domain.enums import SocialPlatforms
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone


class ArtistLinkCollection(ArtistLinkModel, Document):

    id: PydanticObjectId = None
    artist_id: PydanticObjectId
    link: str
    platform: SocialPlatforms
    order: int | None = None
    
    class Settings:
        name = "ArtistLink"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)