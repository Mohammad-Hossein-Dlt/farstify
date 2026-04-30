from src.repo.interface.Idocument_link_repo import IDocumentLinkRepo
from src.models.schemas.filter.sort_direction_filter_input import SortDirectionFilterInput
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
        criteria: SortDirectionFilterInput,
    ) -> list[DocumentLinkModel]:
        
        try:
            links: list[SortDirectionFilterInput] = await self.document_link_repo.get_by_document_id(criteria.value)
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