from pydantic import BaseModel
from src.domain.enums import SocialPlatforms

class CreateLinkInput(BaseModel):
    episode_id: str
    link: str
    platform: SocialPlatforms