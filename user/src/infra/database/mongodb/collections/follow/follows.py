from src.domain.schemas.follow.follow_model import FollowModel
from src.domain.enums import FollowTargetType
from beanie import Document, PydanticObjectId, before_event, Update
from pydantic import Field, model_validator
from bson import ObjectId
from datetime import datetime, timezone


class FollowsCollection(FollowModel, Document):

    id: PydanticObjectId = Field(default_factory=ObjectId)
    user_id: PydanticObjectId
    target_id: PydanticObjectId
    target_type: FollowTargetType
    
    class Settings:
        name = "Follows"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
