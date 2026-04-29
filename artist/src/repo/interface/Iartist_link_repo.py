from abc import ABC, abstractmethod
from src.domain.schemas.artist.artist_link import ArtistLinkModel

class IArtistLinkRepo(ABC):
        
    @abstractmethod
    async def create_link(
        link: ArtistLinkModel,
    ) -> ArtistLinkModel:
    
        raise NotImplementedError               
    
    @abstractmethod
    async def get_link_by_id(
        link_id: str,
    ) ->  ArtistLinkModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update_link(
        link: ArtistLinkModel,
    ) ->  ArtistLinkModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_link(
        link_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_links(
        artist_id: str,
    ) ->  list[ArtistLinkModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_artist_links(
        artist_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all_links() -> bool:
    
        raise NotImplementedError