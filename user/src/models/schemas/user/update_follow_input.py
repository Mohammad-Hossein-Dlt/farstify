from pydantic import BaseModel
from src.domain.enums import FollowTargetType

class UpdateFollowInput(BaseModel):
    id: str
    user_id: str | None = None
    target_id: str | None = None
    target_type: FollowTargetType | None = None