from src.domain.schemas.document.document_link import DocumentLinkModel
from src.domain.enums import SocialPlatforms
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone

class DocumentLinkCollection(DocumentLinkModel, Document):

    id: PydanticObjectId = None
    document_id: PydanticObjectId
    link: str
    platform: SocialPlatforms
    order: int | None = None
    
    class Settings:
        name = "DocumentLink"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
