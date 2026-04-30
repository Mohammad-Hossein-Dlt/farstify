from src.repo.interface.Idocument_link_repo import IDocumentLinkRepo
from src.models.schemas.document.update_link_input import UpdateLinkInput
from src.domain.schemas.document.document_link import DocumentLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateLink:
    
    def __init__(
        self,
        document_link_repo: IDocumentLinkRepo,
    ):

        self.document_link_repo = document_link_repo
    
    async def execute(
        self,
        entity: UpdateLinkInput,
    ) -> DocumentLinkModel:
        
        try:
            link_model: DocumentLinkModel = DocumentLinkModel.model_validate(entity, from_attributes=True)            
            return await self.document_link_repo.update(link_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  