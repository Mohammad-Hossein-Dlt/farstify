from src.domain.schemas.user.user_model import UserModel
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone

class UserCollection(UserModel, Document):

    id: PydanticObjectId = None
    name: str
    user_name: str
    
    class Settings:
        name = "User"

    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)