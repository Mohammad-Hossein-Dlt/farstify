from abc import ABC, abstractmethod
from src.domain.schemas.episode.episode_link import EpisodeLinkModel
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria

class IEpisodeLinkRepo(ABC):
        
    @abstractmethod
    async def create(
        link: EpisodeLinkModel,
    ) -> EpisodeLinkModel:
    
        raise NotImplementedError               
    
    @abstractmethod
    async def get_by_id(
        link_id: str,
    ) -> EpisodeLinkModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        link: EpisodeLinkModel,
    ) -> EpisodeLinkModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        link_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_episode_id(
        episode_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[EpisodeLinkModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_episode_id(
        episode_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError