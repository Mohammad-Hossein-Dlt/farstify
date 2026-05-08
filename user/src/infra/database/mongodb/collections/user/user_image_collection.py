from src.domain.schemas.user.user_image import UserImageModel
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone

class UserImageCollection(UserImageModel, Document):

    id: PydanticObjectId = None
    user_id: PydanticObjectId
    cover: str
    is_main: bool = False
    order: int | None = None
    
    class Settings:
        name = "UserImage"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)