from src.repo.interface.Idocument_link_repo import IDocumentLinkRepo
from src.domain.schemas.document.document_link import DocumentLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class ReorderLinks:
    
    def __init__(
        self,
        document_link_repo: IDocumentLinkRepo,
    ):

        self.document_link_repo = document_link_repo
    
    async def execute(
        self,
        document_id: str,
        link_ids: list[str],
    ) -> DocumentLinkModel:
        
        try:
            links_list: list[DocumentLinkModel] = await self.document_link_repo.get_by_document_id(document_id)
            for index, links_id in enumerate(link_ids):
                for link in links_list:
                    if str(link.id) == links_id:
                        link.order = index
                        await self.document_link_repo.update(link)

            return await self.document_link_repo.get_by_document_id(document_id)        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  