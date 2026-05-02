from abc import ABC, abstractmethod
from src.domain.schemas.document.document_image import DocumentImageModel
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria

class IDocumentImageRepo(ABC):
        
    @abstractmethod
    async def create(
        image: DocumentImageModel,
    ) -> DocumentImageModel:
    
        raise NotImplementedError               
    
    @abstractmethod
    async def get_by_id(
        image_id: str,
    ) -> DocumentImageModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        image: DocumentImageModel,
    ) -> DocumentImageModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        image_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_document_id(
        document_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[DocumentImageModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_document_id(
        document_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError