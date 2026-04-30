from src.domain.schemas.episode.episode_link import EpisodeLinkModel
from src.domain.enums import SocialPlatforms
from beanie import Document, PydanticObjectId, before_event, Update
from pydantic import Field, model_validator
from bson import ObjectId
from datetime import datetime, timezone


class EpisodeLinkCollection(EpisodeLinkModel, Document):

    id: PydanticObjectId = Field(default_factory=ObjectId)
    episode_id: PydanticObjectId
    link: str
    platform: SocialPlatforms
    order: int | None = None
    
    class Settings:
        name = "EpisodeLink"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
