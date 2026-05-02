from src.repo.interface.document.Idocument_link_repo import IDocumentLinkRepo
from document.src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.domain.schemas.document.document_link import DocumentLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllLinks:
    
    def __init__(
        self,
        document_link_repo: IDocumentLinkRepo,
    ):
        
        self.document_link_repo = document_link_repo
    
    async def execute(
        self,
        document_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[DocumentLinkModel]:
        
        try:
            links: list[BaseFilterCriteria] = await self.document_link_repo.get_by_document_id(document_id, criteria)
            if isinstance(links, list):
                if criteria.order == "asc":
                    links.sort(key=lambda x: (x.order is None, x.order))
                elif criteria.order == "desc":
                    links.reverse()
                    links.sort(key=lambda x: (0 if x.order is None else 1, x.order), reverse=True)
            return links
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  