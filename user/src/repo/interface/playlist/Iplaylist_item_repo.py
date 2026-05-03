from abc import ABC, abstractmethod
from src.domain.schemas.playlist.playlist_item_model import PlaylistItemModel
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria

class IPlaylistItemRepo(ABC):
        
    @abstractmethod
    async def create(
        item: PlaylistItemModel,
    ) -> PlaylistItemModel:
    
        raise NotImplementedError        
    
    @abstractmethod
    async def get_by_id(
        item_id: str,
    ) -> PlaylistItemModel:
    
        raise NotImplementedError
        
    @abstractmethod
    async def update(
        item: PlaylistItemModel,
    ) -> PlaylistItemModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        item_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_playlist_id(
        playlist_id: str,
        criteria: BaseFilterCriteria | None = None,
    ) -> list[PlaylistItemModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_playlist_id(
        playlist_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError