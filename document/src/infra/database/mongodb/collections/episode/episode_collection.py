from src.domain.schemas.episode.episode_model import EpisodeModel
from beanie import Document, PydanticObjectId, before_event, Update
from bson import ObjectId
from pydantic import Field, model_validator
from datetime import datetime, timezone


class EpisodeCollection(EpisodeModel, Document):

    id: PydanticObjectId = Field(default_factory=ObjectId)
    document_id: PydanticObjectId = Field(default_factory=ObjectId)
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
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
