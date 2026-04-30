from src.repo.interface.Idocument_link_repo import IDocumentLinkRepo
from src.domain.schemas.document.document_link import DocumentLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetLink:
    
    def __init__(
        self,
        document_link_repo: IDocumentLinkRepo,
    ):
        
        self.document_link_repo = document_link_repo
    
    async def execute(
        self,
        link_id: str,
    ) -> DocumentLinkModel:
        
        try:
            return await self.document_link_repo.get_by_id(link_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  