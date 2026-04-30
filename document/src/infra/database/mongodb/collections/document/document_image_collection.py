from src.domain.schemas.document.document_image import DocumentImageModel
from beanie import Document, PydanticObjectId, before_event, Update
from pydantic import Field, model_validator
from bson import ObjectId
from datetime import datetime, timezone


class DocumentImageCollection(DocumentImageModel, Document):

    id: PydanticObjectId = Field(default_factory=ObjectId)
    document_id: PydanticObjectId
    cover: str
    is_main: bool = False
    order: int | None = None
    
    class Settings:
        name = "DocumentImage"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
