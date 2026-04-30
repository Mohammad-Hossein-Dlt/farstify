from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.repo.interface.document.Idocument_image_repo import IDocumentImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.domain.schemas.document.document_model import DocumentModel
from src.domain.schemas.document.document_image import DocumentImageModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteImage:
    
    def __init__(
        self,
        document_repo: IDocumentRepo,
        document_image_repo: IDocumentImageRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.document_repo = document_repo
        self.document_image_repo = document_image_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        image_id: str,
    ) -> OperationOutput:
        
        try:
            
            image: DocumentImageModel = await self.document_image_repo.get_by_id(image_id)
            document: DocumentModel = await self.document_repo.get_by_id(image.document_id)
            
            result = await self.storage_repo.delete_object(f"{document.id}/" + image.cover)
            
            status = False
            if result:
                status = await self.document_image_repo.delete_by_id(image.id)

            return OperationOutput(id=image_id, request="delete/document-image", status=status)
        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  