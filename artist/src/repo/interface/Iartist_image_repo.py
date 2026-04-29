from abc import ABC, abstractmethod
from src.domain.schemas.artist.artist_image import ArtistImageModel

class IArtistImageRepo(ABC):
        
    @abstractmethod
    async def create_image(
        image: ArtistImageModel,
    ) -> ArtistImageModel:
    
        raise NotImplementedError               
    
    @abstractmethod
    async def get_image_by_id(
        image_id: str,
    ) ->  ArtistImageModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update_image(
        image: ArtistImageModel,
    ) ->  ArtistImageModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_image(
        image_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_images(
        artist_id: str,
    ) ->  list[ArtistImageModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_artist_images(
        artist_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all_images() -> bool:
    
        raise NotImplementedError