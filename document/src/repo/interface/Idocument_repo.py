from abc import ABC, abstractmethod
from src.domain.schemas.document.document_model import DocumentModel

class IDocumentRepo(ABC):
        
    @abstractmethod
    async def create_document(
        document: DocumentModel,
    ) -> DocumentModel:
    
        raise NotImplementedError         
    
    @abstractmethod
    async def get_document_by_name(
        name: str,
    ) -> DocumentModel:
    
        raise NotImplementedError        
    
    @abstractmethod
    async def get_document_by_id(
        document_id: str,
    ) ->  DocumentModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update_document(
        document: DocumentModel,
    ) ->  DocumentModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_document(
        document_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_documents() -> list[DocumentModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all_documents() -> bool:
    
        raise NotImplementedError