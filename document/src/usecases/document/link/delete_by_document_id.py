from src.repo.interface.document.Idocument_link_repo import IDocumentLinkRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllLinks:
    
    def __init__(
        self,
        document_link_repo: IDocumentLinkRepo,
    ):
        
        self.document_link_repo = document_link_repo
    
    async def execute(
        self,
        document_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.document_link_repo.delete_by_document_id(document_id)
            return OperationOutput(id=document_id, request="delete/all-document-links", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  