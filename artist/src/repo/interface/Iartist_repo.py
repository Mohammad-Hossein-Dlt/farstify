from abc import ABC, abstractmethod
from src.domain.schemas.artist.artist_model import ArtistModel

class IArtistRepo(ABC):
        
    @abstractmethod
    async def create_artist(
        artist: ArtistModel,
    ) -> ArtistModel:
    
        raise NotImplementedError         
    
    @abstractmethod
    async def get_artist_by_name(
        name: str,
    ) -> ArtistModel:
    
        raise NotImplementedError        
    
    @abstractmethod
    async def get_artist_by_id(
        artist_id: str,
    ) ->  ArtistModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update_artist(
        artist: ArtistModel,
    ) ->  ArtistModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_artist(
        artist_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_artists() -> list[ArtistModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all_artists() -> bool:
    
        raise NotImplementedError