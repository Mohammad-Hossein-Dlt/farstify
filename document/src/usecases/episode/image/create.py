from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.interface.episode.Iepisode_image_repo import IEpisodeImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.episode.create_image_input import CreateImageInput
from src.domain.schemas.episode.episode_model import EpisodeModel
from src.domain.schemas.episode.episode_image import EpisodeImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
import tempfile
import secrets
from pathlib import Path

class CreateImage:
    
    def __init__(
        self,
        episode_repo: IEpisodeRepo,
        episode_image_repo: IEpisodeImageRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.episode_repo = episode_repo
        self.episode_image_repo = episode_image_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        entity: CreateImageInput,
        file: tempfile.SpooledTemporaryFile | None = None,
        file_name: str | None = None,
        file_size: int | None = None,
        content_type: str | None = None,
    ) -> EpisodeImageModel:
        
        try:
            image_model: EpisodeImageModel = EpisodeImageModel.model_validate(entity, from_attributes=True)
            episode: EpisodeModel = await self.episode_repo.get_by_id(entity.episode_id)
            if all([file, file_name, file_size, content_type]):
                cover_name = secrets.token_hex(nbytes=5) + Path(file_name).suffix
                base_path = f"{episode.document_id}/{episode.id}/image"
                new_object_name = f"{base_path}/{cover_name}"
                try:
                    result = await self.storage_repo.upload_object(
                        file,
                        new_object_name,
                        file_size,
                        content_type,
                    )
                    if result:
                        image_model.cover = cover_name
                        image_model: EpisodeImageModel = await self.episode_image_repo.create(image_model)
                except:
                    if image_model.id:
                        await self.episode_image_repo.delete_by_id(image_model.id)
                    await self.storage_repo.delete_object(new_object_name)

            return image_model
                        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  