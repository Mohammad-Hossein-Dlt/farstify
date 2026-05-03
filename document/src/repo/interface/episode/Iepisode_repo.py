from abc import ABC, abstractmethod
from src.domain.schemas.episode.episode_model import EpisodeModel
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria

class IEpisodeRepo(ABC):
        
    @abstractmethod
    async def create(
        episode: EpisodeModel,
    ) -> EpisodeModel:
    
        raise NotImplementedError    
    
    @abstractmethod
    async def get_by_id(
        episode_id: str,
    ) -> EpisodeModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        episode: EpisodeModel,
    ) -> EpisodeModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        episode_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_document_id(
        document_id: str,
        criteria: BaseFilterCriteria | None = None,
    ) -> list[EpisodeModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_document_id(
        document_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(
        criteria: BaseFilterCriteria | None = None,
    ) -> list[EpisodeModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError