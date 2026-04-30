from src.repo.interface.Idocument_repo import IDocumentRepo
from src.repo.interface.Idocument_image_repo import IDocumentImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.domain.schemas.document.document_model import DocumentModel
from src.domain.schemas.document.document_image import DocumentImageModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllImages:
    
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
        document_id: str,
    ) -> OperationOutput:
        
        try:
            document: DocumentModel = await self.document_repo.get_document_by_id(document_id)
            images: list[DocumentImageModel] = await self.document_image_repo.get_images(document_id)
            
            status = True if images else False
            for i in images:
                result = await self.storage_repo.delete_object(f"{document.id}/" + i.cover)
                if result:
                    await self.document_image_repo.delete_image(i.id)
                else:
                    status = False
            
            return OperationOutput(id=document_id, request="delete/all-document-images", status=status)        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  