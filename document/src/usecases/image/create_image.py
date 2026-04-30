from src.repo.interface.Idocument_repo import IDocumentRepo
from src.repo.interface.Idocument_image_repo import IDocumentImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.document.create_image_input import CreateImageInput
from src.domain.schemas.document.document_model import DocumentModel
from src.domain.schemas.document.document_image import DocumentImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
from pathlib import Path
import tempfile
import secrets

class CreateImage:
    
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
        to_create: CreateImageInput,
        file: tempfile.SpooledTemporaryFile | None = None,
        file_name: str | None = None,
        file_size: int | None = None,
        content_type: str | None = None,
    ) -> DocumentImageModel:
        
        try:
            
            document: DocumentModel = await self.document_repo.get_document_by_id(to_create.document_id)
            image: DocumentImageModel = DocumentImageModel.model_validate(to_create, from_attributes=True)

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
                        image.cover = cover_name
                        image: DocumentImageModel = await self.document_image_repo.create_image(image)
                except:
                    if image.id:
                        await self.document_image_repo.delete_image(image.id)
                    await self.storage_repo.delete_object(f"{document.id}/" + cover_name)

            return image
                        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  