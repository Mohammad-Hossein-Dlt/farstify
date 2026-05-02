from abc import ABC, abstractmethod
from src.domain.schemas.user.user_image import UserImageModel
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria

class IUserImageRepo(ABC):
        
    @abstractmethod
    async def create(
        image: UserImageModel,
    ) -> UserImageModel:
    
        raise NotImplementedError           
    
    @abstractmethod
    async def get_by_id(
        image_id: str,
    ) -> UserImageModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        image: UserImageModel,
    ) -> UserImageModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        image_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_user_id(
        user_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[UserImageModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_user_id(
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError