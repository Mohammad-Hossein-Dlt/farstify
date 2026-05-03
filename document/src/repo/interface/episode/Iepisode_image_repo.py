from abc import ABC, abstractmethod
from src.domain.schemas.episode.episode_image import EpisodeImageModel
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria

class IEpisodeImageRepo(ABC):
        
    @abstractmethod
    async def create(
        image: EpisodeImageModel,
    ) -> EpisodeImageModel:
    
        raise NotImplementedError               
    
    @abstractmethod
    async def get_by_id(
        image_id: str,
    ) -> EpisodeImageModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        image: EpisodeImageModel,
    ) -> EpisodeImageModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        image_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_episode_id(
        episode_id: str,
        criteria: BaseFilterCriteria | None = None,
    ) -> list[EpisodeImageModel]:

        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_episode_id(
        episode_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError