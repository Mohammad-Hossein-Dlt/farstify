from src.domain.schemas.user.user_link import UserLinkModel
from src.domain.enums import SocialPlatforms
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone

class UserLinkCollection(UserLinkModel, Document):

    id: PydanticObjectId = None
    user_id: PydanticObjectId
    link: str
    platform: SocialPlatforms
    order: int | None = None
    
    class Settings:
        name = "UserLink"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)