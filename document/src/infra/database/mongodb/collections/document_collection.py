from src.domain.schemas.document.document_model import DocumentModel
from beanie import Document, PydanticObjectId, before_event, Update
from bson import ObjectId
from pydantic import Field, model_validator
from datetime import datetime, timezone


class DocumentCollection(DocumentModel, Document):

    id: PydanticObjectId = Field(default_factory=ObjectId)
    name: str
    description: str | None = None
    active: bool | None = None
    
    class Settings:
        name = "Document"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
