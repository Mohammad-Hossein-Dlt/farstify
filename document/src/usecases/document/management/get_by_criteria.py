from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.domain.schemas.document.document_model import DocumentModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllDocuments:
    
    def __init__(
        self,
        document_repo: IDocumentRepo,
    ):
        
        self.document_repo = document_repo  
    
    async def execute(
        self,
        criteria: BaseFilterCriteria,
    ) -> list[DocumentModel]:
        
        try:
            return await self.document_repo.get_all(criteria)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  