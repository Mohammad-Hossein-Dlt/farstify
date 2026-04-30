from abc import ABC, abstractmethod
from src.domain.schemas.document.document_link import DocumentLinkModel

class IDocumentLinkRepo(ABC):
        
    @abstractmethod
    async def create_link(
        link: DocumentLinkModel,
    ) -> DocumentLinkModel:
    
        raise NotImplementedError               
    
    @abstractmethod
    async def get_link_by_id(
        link_id: str,
    ) ->  DocumentLinkModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update_link(
        link: DocumentLinkModel,
    ) ->  DocumentLinkModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_link(
        link_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_links(
        document_id: str,
    ) ->  list[DocumentLinkModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_document_links(
        document_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all_links() -> bool:
    
        raise NotImplementedError