from src.domain.schemas.follow.follow_model import FollowModel
from src.domain.enums import FollowTargetType
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone

class FollowsCollection(FollowModel, Document):

    id: PydanticObjectId = None
    user_id: PydanticObjectId
    target_id: PydanticObjectId
    target_type: FollowTargetType
    
    class Settings:
        name = "Follows"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)