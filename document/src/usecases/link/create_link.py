from src.repo.interface.Idocument_repo import IDocumentRepo
from src.repo.interface.Idocument_link_repo import IDocumentLinkRepo
from src.models.schemas.document.create_link_input import CreateLinkInput
from src.domain.schemas.document.document_link import DocumentLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateLink:
    
    def __init__(
        self,
        document_repo: IDocumentRepo,
        document_link_repo: IDocumentLinkRepo,
    ):
        
        self.document_repo = document_repo
        self.document_link_repo = document_link_repo
    
    async def execute(
        self,
        to_create: CreateLinkInput,
    ) -> DocumentLinkModel:
        
        try:
            await self.document_repo.get_document_by_id(to_create.document_id)
            link_model: DocumentLinkModel = DocumentLinkModel.model_validate(to_create, from_attributes=True)
            return await self.document_link_repo.create_link(link_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  