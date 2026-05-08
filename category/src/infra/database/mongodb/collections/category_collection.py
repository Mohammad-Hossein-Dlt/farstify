from src.domain.schemas.category.category_model import CategoryModel
from beanie import Document, PydanticObjectId

class CategoryCollection(CategoryModel, Document):

    id: PydanticObjectId = None
    parent_id: PydanticObjectId | None = None
    slug: str
    name: str    
    cover:str | None = None
    
    class Settings:
        name = "Category"