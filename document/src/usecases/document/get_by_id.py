from src.repo.interface.Idocument_repo import IDocumentRepo
from src.domain.schemas.document.document_model import DocumentModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetDocument:
    
    def __init__(
        self,
        document_repo: IDocumentRepo,
    ):
        
        self.document_repo = document_repo  
    
    async def execute(
        self,
        document_id: str,
    ) -> DocumentModel:
        
        try:
            return await self.document_repo.get_by_id(document_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")