from src.repo.interface.Idocument_repo import IDocumentRepo
from src.repo.interface.Idocument_image_repo import IDocumentImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.document.update_image_input import UpdateImageInput
from src.domain.schemas.document.document_model import DocumentModel
from src.domain.schemas.document.document_image import DocumentImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
import tempfile
import secrets
from pathlib import Path

class UpdateImage:
    
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
        entity: UpdateImageInput,
        file: tempfile.SpooledTemporaryFile | None = None,
        file_name: str | None = None,
        file_size: int | None = None,
        content_type: str | None = None,
    ) -> DocumentImageModel:
        
        try:
            image_model: DocumentImageModel = DocumentImageModel.model_validate(entity, from_attributes=True)
            image: DocumentImageModel = await self.document_image_repo.get_by_id(entity.id)
            document: DocumentModel = await self.document_repo.get_by_id(image.document_id)
            pre_cover = image.cover
            if all([file, file_name, file_size, content_type]):
                try:
                    cover_name = secrets.token_hex(nbytes=5) + Path(file_name).suffix
                    result = await self.storage_repo.upload_object(
                        file,
                        f"{document.id}/" + cover_name,
                        file_size,
                        content_type,
                    )      
                    if result:
                        image_model.cover = cover_name
                        image: DocumentImageModel = await self.document_image_repo.update(image_model)
                        await self.storage_repo.delete_object(f"{document.id}/" + pre_cover)
                except:
                    image.cover = pre_cover
                    image: DocumentImageModel = await self.document_image_repo.update(image)
                    await self.storage_repo.delete_object(f"{document.id}/" + cover_name)
            else:
                image: DocumentImageModel = await self.document_image_repo.update(image_model)

            return image
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  