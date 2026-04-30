from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.repo.interface.document.Idocument_image_repo import IDocumentImageRepo
from src.repo.interface.document.Idocument_link_repo import IDocumentLinkRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.domain.schemas.document.document_model import DocumentModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteDocument:
    
    def __init__(
        self,
        document_repo: IDocumentRepo,
        document_image_repo: IDocumentImageRepo,
        document_link_repo: IDocumentLinkRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.document_repo = document_repo
        self.document_image_repo = document_image_repo
        self.document_link_repo = document_link_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        document_id: str,
    ) -> OperationOutput:
        
        try:
            status = False
            document: DocumentModel = await self.document_repo.get_by_id(document_id)
            check_path = await self.storage_repo.path_objects(str(document.id))
            if check_path:
                delete_objects = await self.storage_repo.delete_objects(str(document.id))
                if delete_objects:
                    await self.document_image_repo.delete_by_document_id(document_id)
                    await self.document_link_repo.delete_by_document_id(document_id)
                    status = await self.document_repo.delete_by_id(document_id)
            else:
                await self.document_image_repo.delete_by_document_id(document_id)
                await self.document_link_repo.delete_by_document_id(document_id)
                status = await self.document_repo.delete_by_id(document_id)
            
            return OperationOutput(id=document_id, request="delete/document", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  