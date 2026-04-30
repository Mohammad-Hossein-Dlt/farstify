from src.repo.interface.Idocument_repo import IDocumentRepo
from src.repo.interface.Idocument_image_repo import IDocumentImageRepo
from src.domain.schemas.document.document_image import DocumentImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class ReorderImages:
    
    def __init__(
        self,
        document_repo: IDocumentRepo,
        document_image_repo: IDocumentImageRepo,
    ):
        
        self.document_repo = document_repo
        self.document_image_repo = document_image_repo
    
    async def execute(
        self,
        document_id: str,
        image_ids: list[str],
    ) -> list[DocumentImageModel]:
        
        try:
            images_list: list[DocumentImageModel] = await self.document_image_repo.get_by_document_id(document_id)
            for index, image_id in enumerate(image_ids):
                for image in images_list:
                    if str(image.id) == image_id:
                        image.order = index
                        await self.document_image_repo.update(image)

            return await self.document_image_repo.get_by_document_id(document_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  