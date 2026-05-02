from pydantic import BaseModel

class LikeInput(BaseModel):
    user_id: str
    episode_id: str