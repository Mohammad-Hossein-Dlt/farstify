from src.repo.interface.Iartist_repo import IArtistRepo
from src.repo.interface.Iartist_image_repo import IArtistImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.artist.update_image_input import UpdateImageInput
from src.domain.schemas.artist.artist_model import ArtistModel
from src.domain.schemas.artist.artist_image import ArtistImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
import tempfile
import secrets
from pathlib import Path

class UpdateImage:
    
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
        entity: UpdateImageInput,
        file: tempfile.SpooledTemporaryFile | None = None,
        file_name: str | None = None,
        file_size: int | None = None,
        content_type: str | None = None,
    ) -> ArtistImageModel:
        
        try:
            image_model: ArtistImageModel = ArtistImageModel.model_validate(entity, from_attributes=True)
            image: ArtistImageModel = await self.artist_image_repo.get_by_id(entity.id)
            artist: ArtistModel = await self.artist_repo.get_by_id(image.artist_id)
            prev_cover = image.cover
            if all([file, file_name, file_size, content_type]):
                cover_name = secrets.token_hex(nbytes=5) + Path(file_name).suffix
                base_path = f"{artist.id}/image"
                new_object_name = f"{base_path}/{cover_name}"
                prev_object_name = f"{base_path}/{prev_cover}"
                try:
                    result = await self.storage_repo.upload_object(
                        file,
                        new_object_name,
                        file_size,
                        content_type,
                    )      
                    if result:
                        image_model.cover = cover_name
                        image: ArtistImageModel = await self.artist_image_repo.update(image_model)
                        await self.storage_repo.delete_object(prev_object_name)
                except:
                    image.cover = prev_cover
                    image: ArtistImageModel = await self.artist_image_repo.update(image)
                    await self.storage_repo.delete_object(new_object_name)
            else:
                image: ArtistImageModel = await self.artist_image_repo.update(image_model)

            return image
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  