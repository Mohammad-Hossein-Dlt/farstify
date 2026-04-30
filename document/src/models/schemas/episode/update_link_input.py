from pydantic import BaseModel
from src.domain.enums import SocialPlatforms

class UpdateLinkInput(BaseModel):
    id: str
    link: str | None = None
    platform: SocialPlatforms | None = None