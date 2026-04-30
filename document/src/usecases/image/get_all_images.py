from src.repo.interface.Idocument_repo import IDocumentRepo
from src.repo.interface.Idocument_image_repo import IDocumentImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.filter.sort_direction_filter_input import SortDirectionFilterInput
from src.domain.schemas.document.document_image import DocumentImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllImages:
    
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
        to_filter: SortDirectionFilterInput,
    ) -> list[DocumentImageModel]:
        
        try:
            images: list[DocumentImageModel] = await self.document_image_repo.get_images(to_filter.value)
            if isinstance(images, list):
                if to_filter.order == "asc":
                    images.sort(key=lambda x: (x.order is None, x.order))
                elif to_filter.order == "desc":
                    images.reverse()
                    images.sort(key=lambda x: (0 if x.order is None else 1, x.order), reverse=True)
            return images
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  