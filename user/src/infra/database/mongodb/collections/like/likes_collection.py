from src.domain.schemas.like.like_model import LikeModel
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone

class LikesCollection(LikeModel, Document):

    id: PydanticObjectId = None
    user_id: PydanticObjectId
    episode_id: PydanticObjectId
    
    class Settings:
        name = "Likes"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)