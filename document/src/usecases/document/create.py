from src.repo.interface.Idocument_repo import IDocumentRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.document.create_document_input import CreateDocumentInput
from src.domain.schemas.document.document_model import DocumentModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateDocument:
    
    def __init__(
        self,
        document_repo: IDocumentRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.document_repo = document_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        entity: CreateDocumentInput,
    ) -> DocumentModel:
        
        try:
            document_model: DocumentModel = DocumentModel.model_validate(entity, from_attributes=True)
            return await self.document_repo.create(document_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  