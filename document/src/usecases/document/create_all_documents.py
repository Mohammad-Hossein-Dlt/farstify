from src.repo.interface.Idocument_repo import IDocumentRepo
from src.models.schemas.document.create_document_input import CreateDocumentInput
from src.domain.schemas.document.document_model import DocumentModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateAllDocuments:
    
    def __init__(
        self,
        document_repo: IDocumentRepo,
    ):
        
        self.document_repo = document_repo
    
    async def execute(
        self,
        documents: list[CreateDocumentInput],
    ) -> DocumentModel:
        
        for document in documents:
            
            try:
                document = DocumentModel.model_validate(document, from_attributes=True)
                await self.document_repo.create_document(document)
            except AppBaseException:
                raise
            except:
                raise OperationFailureException(500, "Internal server error")
            
        return OperationOutput(id=None, request="create/all_document", status=True)