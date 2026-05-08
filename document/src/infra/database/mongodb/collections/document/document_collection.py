from src.domain.schemas.document.document_model import DocumentModel
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone

class DocumentCollection(DocumentModel, Document):

    id: PydanticObjectId = None
    title: str
    description: str | None = None
    single: bool = False
    active: bool = False
    
    class Settings:
        name = "Document"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)