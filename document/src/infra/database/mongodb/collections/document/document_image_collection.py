from src.domain.schemas.document.document_image import DocumentImageModel
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone

class DocumentImageCollection(DocumentImageModel, Document):

    id: PydanticObjectId = None
    document_id: PydanticObjectId
    cover: str
    is_main: bool = False
    order: int | None = None
    
    class Settings:
        name = "DocumentImage"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)