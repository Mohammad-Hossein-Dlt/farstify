from pydantic import BaseModel
from src.domain.enums import FollowTargetType

class CreateFollowInput(BaseModel):
    user_id: str
    target_id: str
    target_type: FollowTargetType