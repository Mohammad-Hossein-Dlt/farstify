from abc import ABC, abstractmethod
from src.domain.schemas.artist.artist_model import ArtistModel

class IArtistRepo(ABC):
        
    @abstractmethod
    async def create(
        artist: ArtistModel,
    ) -> ArtistModel:
    
        raise NotImplementedError         
    
    @abstractmethod
    async def get_by_name(
        name: str,
    ) -> ArtistModel:
    
        raise NotImplementedError        
    
    @abstractmethod
    async def get_by_id(
        artist_id: str,
    ) ->  ArtistModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        artist: ArtistModel,
    ) ->  ArtistModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        artist_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_all() -> list[ArtistModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError