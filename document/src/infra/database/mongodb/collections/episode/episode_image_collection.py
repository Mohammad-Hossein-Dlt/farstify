from src.domain.schemas.episode.episode_image import EpisodeImageModel
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone

class EpisodeImageCollection(EpisodeImageModel, Document):

    id: PydanticObjectId = None
    episode_id: PydanticObjectId
    cover: str
    is_main: bool = False
    order: int | None = None
    
    class Settings:
        name = "EpisodeImage"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)