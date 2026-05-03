from abc import ABC, abstractmethod
from src.domain.schemas.like.like_model import LikeModel
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria

class ILikesRepo(ABC):
        
    @abstractmethod
    async def create(
        like: LikeModel,
    ) -> LikeModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def check_unique(
        like: LikeModel,
    ) -> LikeModel:
    
        raise NotImplementedError           
    
    @abstractmethod
    async def get_by_id(
        like_id: str,
    ) -> LikeModel:
    
        raise NotImplementedError
        
    @abstractmethod
    async def update(
        like: LikeModel,
    ) -> LikeModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        like_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_user_id(
        user_id: str,
        criteria: BaseFilterCriteria | None = None,
    ) -> list[LikeModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_user_id(
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError