from src.domain.schemas.episode.episode_model import EpisodeModel
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone

class EpisodeCollection(EpisodeModel, Document):

    id: PydanticObjectId = None
    document_id: PydanticObjectId
    title: str
    description: str | None = None
    duration: float | None = None
    active: bool = False
    order: int | None = None
    
    class Settings:
        name = "Episode"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
