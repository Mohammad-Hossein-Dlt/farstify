from abc import ABC, abstractmethod
from src.domain.schemas.document.document_image import DocumentImageModel

class IDocumentImageRepo(ABC):
        
    @abstractmethod
    async def create_image(
        image: DocumentImageModel,
    ) -> DocumentImageModel:
    
        raise NotImplementedError               
    
    @abstractmethod
    async def get_image_by_id(
        image_id: str,
    ) ->  DocumentImageModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update_image(
        image: DocumentImageModel,
    ) ->  DocumentImageModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_image(
        image_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_images(
        document_id: str,
    ) ->  list[DocumentImageModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_document_images(
        document_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all_images() -> bool:
    
        raise NotImplementedError