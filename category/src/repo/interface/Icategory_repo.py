from abc import ABC, abstractmethod
from src.domain.schemas.category.category_model import CategoryModel
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput

class ICategoryRepo(ABC):
        
    @abstractmethod
    async def create(
        category: CategoryModel,
    ) -> CategoryModel:
    
        raise NotImplementedError         
    
    @abstractmethod
    async def check_unique(
        category: CategoryModel,
    ) -> CategoryModel:
    
        raise NotImplementedError        

    @abstractmethod
    async def get_by_id(
        category_id: str,
    ) -> CategoryModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        category: CategoryModel,
    ) -> CategoryModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        category_id: str,
    ) -> bool:
    
        raise NotImplementedError

    @abstractmethod
    async def get_all() -> list[CategoryModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_criteria(
        criteria: CategoryFilterInput,
    ) -> list[CategoryModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_tree_from_parent(
        criteria: CategoryFilterInput,
    ) -> list[CategoryModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_ancestors(
        parent_id: str,
    ) -> list[CategoryModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_parent_id(
        parent_id: str | None = None,
        contains_danglings: bool = False, 
    ) -> list[CategoryModel]:
    
        raise NotImplementedError
        
    @abstractmethod
    async def get_descendants(
        parent_id: str,
    ) -> list[CategoryModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_parent_id(
        parent_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError