from abc import ABC, abstractmethod
from src.domain.schemas.document.document_link import DocumentLinkModel

class IDocumentLinkRepo(ABC):
        
    @abstractmethod
    async def create(
        link: DocumentLinkModel,
    ) -> DocumentLinkModel:
    
        raise NotImplementedError               
    
    @abstractmethod
    async def get_by_id(
        link_id: str,
    ) -> DocumentLinkModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        link: DocumentLinkModel,
    ) -> DocumentLinkModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        link_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_document_id(
        document_id: str,
    ) -> list[DocumentLinkModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_document_id(
        document_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError