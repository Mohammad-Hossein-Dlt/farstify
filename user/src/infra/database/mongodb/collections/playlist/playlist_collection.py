from src.domain.schemas.playlist.playlist_model import PlaylistModel
from beanie import Document, PydanticObjectId, before_event, Update
from pydantic import Field, model_validator
from bson import ObjectId
from datetime import datetime, timezone


class PlaylistCollection(PlaylistModel, Document):

    id: PydanticObjectId = Field(default_factory=ObjectId)
    user_id: PydanticObjectId
    cover: str | None = None
    title: str
    description: str | None = None
    public: bool
    
    class Settings:
        name = "Playlist"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
