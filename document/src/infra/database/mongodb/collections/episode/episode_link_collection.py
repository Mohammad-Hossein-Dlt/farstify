from src.domain.schemas.episode.episode_link import EpisodeLinkModel
from src.domain.enums import SocialPlatforms
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone

class EpisodeLinkCollection(EpisodeLinkModel, Document):

    id: PydanticObjectId = None
    episode_id: PydanticObjectId
    link: str
    platform: SocialPlatforms
    order: int | None = None
    
    class Settings:
        name = "EpisodeLink"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
