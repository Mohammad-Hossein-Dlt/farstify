from abc import ABC, abstractmethod
from src.domain.schemas.playlist.playlist_model import PlaylistModel
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria

class IPlaylistRepo(ABC):
        
    @abstractmethod
    async def create(
        playlist: PlaylistModel,
    ) -> PlaylistModel:
    
        raise NotImplementedError        
    
    @abstractmethod
    async def get_by_id(
        playlist_id: str,
    ) -> PlaylistModel:
    
        raise NotImplementedError
        
    @abstractmethod
    async def update(
        playlist: PlaylistModel,
    ) -> PlaylistModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        playlist_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_user_id(
        user_id: str,
        criteria: BaseFilterCriteria | None = None,
    ) -> list[PlaylistModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_user_id(
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError