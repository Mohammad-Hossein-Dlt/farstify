from src.infra.utils.custom_base_model import CustomBaseModel
from src.domain.enums import SocialPlatforms
from pydantic import Field, ConfigDict, model_validator
from beanie import PydanticObjectId
from datetime import datetime, timezone
from typing import Self

class ArtistLinkModel(CustomBaseModel):
    
    id: int | PydanticObjectId | None = None
    artist_id: int | PydanticObjectId | None = None
    link: str | None = None
    platform: SocialPlatforms | None = None
    order: int | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(
        extra='allow',
        populate_by_name=True,
    )

    @model_validator(mode='after')
    def validate_values(
        self
    ) -> Self:
        
        if "updated_at" not in self.model_fields_set:
            self.updated_at = self.created_at
        
        return self