from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.repo.interface.document.Idocument_image_repo import IDocumentImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.domain.schemas.document.document_image import DocumentImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetImage:
    
    def __init__(
        self,
        document_repo: IDocumentRepo,
        document_image_repo: IDocumentImageRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.document_repo = document_repo
        self.document_image_repo = document_image_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        image_id: str,
    ) -> DocumentImageModel:
        
        try:
            return await self.document_image_repo.get_by_id(image_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  