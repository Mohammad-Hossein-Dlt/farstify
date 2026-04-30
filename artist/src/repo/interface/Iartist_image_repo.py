from abc import ABC, abstractmethod
from src.domain.schemas.artist.artist_image import ArtistImageModel

class IArtistImageRepo(ABC):
        
    @abstractmethod
    async def create(
        image: ArtistImageModel,
    ) -> ArtistImageModel:
    
        raise NotImplementedError           
    
    @abstractmethod
    async def get_by_id(
        image_id: str,
    ) ->  ArtistImageModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        image: ArtistImageModel,
    ) ->  ArtistImageModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        image_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_artist_id(
        artist_id: str,
    ) ->  list[ArtistImageModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_artist_id(
        artist_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError