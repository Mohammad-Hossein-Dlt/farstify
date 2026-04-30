from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.repo.interface.document.Idocument_image_repo import IDocumentImageRepo
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
        entity: CreateImageInput,
        file: tempfile.SpooledTemporaryFile | None = None,
        file_name: str | None = None,
        file_size: int | None = None,
        content_type: str | None = None,
    ) -> DocumentImageModel:
        
        try:
            
            document: DocumentModel = await self.document_repo.get_by_id(entity.document_id)
            image_model: DocumentImageModel = DocumentImageModel.model_validate(entity, from_attributes=True)

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
                        image_model: DocumentImageModel = await self.document_image_repo.create(image_model)
                except:
                    if image_model.id:
                        await self.document_image_repo.delete_by_id(image_model.id)
                    await self.storage_repo.delete_object(f"{document.id}/" + cover_name)

            return image_model
                        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  