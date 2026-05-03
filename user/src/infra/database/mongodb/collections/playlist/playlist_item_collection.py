from src.domain.schemas.playlist.playlist_item_model import PlaylistItemModel
from beanie import Document, PydanticObjectId, before_event, Update
from pydantic import Field, model_validator
from bson import ObjectId
from datetime import datetime, timezone

class PlaylistItemCollection(PlaylistItemModel, Document):

    id: PydanticObjectId = Field(default_factory=ObjectId)
    playlist_id: PydanticObjectId
    episode_id: PydanticObjectId
    order: int | None = None
    
    class Settings:
        name = "Playlist_Item"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
