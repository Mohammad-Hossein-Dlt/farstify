from src.repo.interface.Iartist_repo import IArtistRepo
from src.repo.interface.Iartist_image_repo import IArtistImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.artist.create_image_input import CreateImageInput
from src.domain.schemas.artist.artist_model import ArtistModel
from src.domain.schemas.artist.artist_image import ArtistImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
from pathlib import Path
import tempfile
import secrets

class CreateImage:
    
    def __init__(
        self,
        artist_repo: IArtistRepo,
        artist_image_repo: IArtistImageRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.artist_repo = artist_repo
        self.artist_image_repo = artist_image_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        entity: CreateImageInput,
        file: tempfile.SpooledTemporaryFile | None = None,
        file_name: str | None = None,
        file_size: int | None = None,
        content_type: str | None = None,
    ) -> ArtistImageModel:
        
        try:
            
            artist: ArtistModel = await self.artist_repo.get_by_id(entity.artist_id)
            image_model: ArtistImageModel = ArtistImageModel.model_validate(entity, from_attributes=True)

            if all([file, file_name, file_size, content_type]):
                
                try:
                    cover_name = secrets.token_hex(nbytes=5) + Path(file_name).suffix
                    result = await self.storage_repo.upload_object(
                        file,
                        f"{artist.id}/" + cover_name,
                        file_size,
                        content_type,
                    )
                    if result:
                        image_model.cover = cover_name
                        image_model: ArtistImageModel = await self.artist_image_repo.create(image_model)
                except:
                    if image_model.id:
                        await self.artist_image_repo.delete_by_id(image_model.id)
                    await self.storage_repo.delete_object(f"{artist.id}/" + cover_name)

            return image_model
                        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  