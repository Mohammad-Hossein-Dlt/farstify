from src.repo.interface.Idocument_link_repo import IDocumentLinkRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteLink:
    
    def __init__(
        self,
        document_link_repo: IDocumentLinkRepo,
    ):
        
        self.document_link_repo = document_link_repo
    
    async def execute(
        self,
        link_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.document_link_repo.delete_by_id(link_id)
            return OperationOutput(id=link_id, request="delete/document-link", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  