from abc import ABC, abstractmethod
from src.domain.schemas.user.user_model import UserModel
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria

class IUserRepo(ABC):
        
    @abstractmethod
    async def create(
        user: UserModel,
    ) -> UserModel:
    
        raise NotImplementedError         
    
    @abstractmethod
    async def get_by_name(
        name: str,
    ) -> UserModel:
    
        raise NotImplementedError        
    
    @abstractmethod
    async def get_by_id(
        user_id: str,
    ) -> UserModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        user: UserModel,
    ) -> UserModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(
        criteria: BaseFilterCriteria | None = None,
    ) -> list[UserModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError