from src.infra.utils.custom_base_model import CustomBaseModel
from pydantic import ConfigDict, Field, model_validator
from beanie import PydanticObjectId
from datetime import datetime, timezone
from typing import Self

class ArtistModel(CustomBaseModel):
    
    id: int | PydanticObjectId | None = None
    name: str | None = None
    description: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(
        extra='allow',
    )
    
    @model_validator(mode='after')
    def validate_values(
        self
    ) -> Self:
        
        if "updated_at" not in self.model_fields_set:
            self.updated_at = self.created_at
        
        return self
        
    # def get_image_by_id(
    #     self,
    #     image_id: str,
    # ) -> ArtistImageModel | None:
    #     for i in self.images:
    #         if str(i.id) == image_id:
    #             return i.model_copy()
    #     return None
    
    # def update_image(
    #     self,
    #     image_id: str,
    #     cover_name: str | None = None,
    #     is_main: bool | None = None,
    # ) -> ArtistImageModel | None:
        
    #     for i in self.images:
    #         if str(i.id) == image_id:
                
    #             if cover_name is not None:
    #                 i.cover = cover_name
                    
    #             if is_main is not None:
    #                 i.is_main = is_main
                    
    #             return i
            
    #     return None
    
    # def remove_image_by_name(
    #     self,
    #     cover_name: str,
    # ):
    #     for i in self.images:
    #         if i.cover == cover_name:
    #             self.images.remove(i)
                
    # def remove_image_by_id(
    #     self,
    #     image_id: str,
    # ):
    #     for i in self.images:
    #         if str(i.id) == image_id:
    #             self.images.remove(i)
                
    # def get_link_by_id(
    #     self,
    #     link_id: str,
    # ) -> ArtistLinkModel | None:
    #     for i in self.links:
    #         if str(i.id) == link_id:
    #             return i.model_copy()
    #     return None
    
    # def update_link(
    #     self,
    #     link_id: str,
    #     link: str | None = None,
    #     platform: SocialPlatforms = None,
    # ) -> ArtistLinkModel | None:
        
    #     for i in self.links:
    #         if str(i.id) == link_id:
                
    #             if link is not None:
    #                 i.link = link
                    
    #             if platform is not None:
    #                 i.platform = platform
                    
    #             return i
            
    #     return None
                
    # def remove_link_by_id(
    #     self,
    #     link_id: str,
    # ):
    #     for i in self.links:
    #         if str(i.id) == link_id:
    #             self.links.remove(i)