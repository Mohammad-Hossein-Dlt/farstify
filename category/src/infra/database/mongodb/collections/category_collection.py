from src.domain.schemas.category.category_model import CategoryModel
from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import Field, model_validator

class CategoryCollection(CategoryModel, Document):

    id: PydanticObjectId = Field(default_factory=ObjectId)
    parent_id: PydanticObjectId | None = None
    slug: str
    name: str    
    cover:str | None = None
    
    class Settings:
        name = "Category"
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
