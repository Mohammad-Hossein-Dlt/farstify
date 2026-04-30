from abc import ABC, abstractmethod
from src.domain.schemas.episode.episode_model import EpisodeModel

class IEpisodeRepo(ABC):
        
    @abstractmethod
    async def create(
        episode: EpisodeModel,
    ) -> EpisodeModel:
    
        raise NotImplementedError    
    
    @abstractmethod
    async def get_by_id(
        episode_id: str,
    ) ->  EpisodeModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        episode: EpisodeModel,
    ) ->  EpisodeModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        episode_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_all() -> list[EpisodeModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError