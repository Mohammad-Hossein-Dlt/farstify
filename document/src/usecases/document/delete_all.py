from src.repo.interface.Idocument_repo import IDocumentRepo
from src.repo.interface.Idocument_image_repo import IDocumentImageRepo
from src.repo.interface.Idocument_link_repo import IDocumentLinkRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllDocuments:
    
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
    ) -> OperationOutput:
        
        try:
            status = await self.storage_repo.clean_dir()
            if status:
                await self.document_image_repo.delete_all()
                await self.document_link_repo.delete_all()
                status = await self.document_repo.delete_all()                    
            
            return OperationOutput(id=None, request="delete/all_documents", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  