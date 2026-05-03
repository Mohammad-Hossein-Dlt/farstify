from abc import ABC, abstractmethod
from src.domain.schemas.follow.follow_model import FollowModel
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria

class IFollowsRepo(ABC):
        
    @abstractmethod
    async def create(
        follow: FollowModel,
    ) -> FollowModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def check_unique(
        follow: FollowModel,
    ) -> FollowModel:
    
        raise NotImplementedError           
    
    @abstractmethod
    async def get_by_id(
        follow_id: str,
    ) -> FollowModel:
    
        raise NotImplementedError
        
    @abstractmethod
    async def update(
        follow: FollowModel,
    ) -> FollowModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        follow_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_user_id(
        user_id: str,
        criteria: BaseFilterCriteria | None = None,
    ) -> list[FollowModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_user_id(
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError