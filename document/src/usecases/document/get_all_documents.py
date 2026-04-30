from src.repo.interface.Idocument_repo import IDocumentRepo
from src.models.schemas.filter.sort_direction_filter_input import SortDirectionFilterInput
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
        to_filter: SortDirectionFilterInput,
    ) -> list[DocumentModel]:
        
        try:
            documents: list[DocumentModel] = await self.document_repo.get_all_documents()
            if isinstance(documents, list):
                if to_filter.order == "asc":
                    pass
                elif to_filter.order == "desc":
                    documents.reverse()
            return documents
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  