from abc import ABC, abstractmethod
from src.domain.schemas.artist.artist_link import ArtistLinkModel

class IArtistLinkRepo(ABC):
        
    @abstractmethod
    async def create(
        link: ArtistLinkModel,
    ) -> ArtistLinkModel:
    
        raise NotImplementedError               
    
    @abstractmethod
    async def get_by_id(
        link_id: str,
    ) ->  ArtistLinkModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        link: ArtistLinkModel,
    ) ->  ArtistLinkModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        link_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_artist_id(
        artist_id: str,
    ) ->  list[ArtistLinkModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_artist_id(
        artist_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError