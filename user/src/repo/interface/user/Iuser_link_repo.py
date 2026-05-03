from abc import ABC, abstractmethod
from src.domain.schemas.user.user_link import UserLinkModel
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria

class IUserLinkRepo(ABC):
        
    @abstractmethod
    async def create(
        link: UserLinkModel,
    ) -> UserLinkModel:
    
        raise NotImplementedError               
    
    @abstractmethod
    async def get_by_id(
        link_id: str,
    ) -> UserLinkModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        link: UserLinkModel,
    ) -> UserLinkModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        link_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_user_id(
        user_id: str,
        criteria: BaseFilterCriteria | None = None,
    ) -> list[UserLinkModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_user_id(
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError