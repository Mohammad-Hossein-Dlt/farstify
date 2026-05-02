from abc import ABC, abstractmethod
from src.domain.schemas.document.document_model import DocumentModel
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria

class IDocumentRepo(ABC):
        
    @abstractmethod
    async def create(
        document: DocumentModel,
    ) -> DocumentModel:
    
        raise NotImplementedError    
    
    @abstractmethod
    async def get_by_id(
        document_id: str,
    ) -> DocumentModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        document: DocumentModel,
    ) -> DocumentModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        document_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_artist_id(
        artist_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[DocumentModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_artist_id(
        artist_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(
        criteria: BaseFilterCriteria,
    ) -> list[DocumentModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError