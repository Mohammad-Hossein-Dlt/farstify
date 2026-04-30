from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.interface.episode.Iepisode_image_repo import IEpisodeImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.episode.update_image_input import UpdateImageInput
from src.domain.schemas.episode.episode_model import EpisodeModel
from src.domain.schemas.episode.episode_image import EpisodeImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
import tempfile
import secrets
from pathlib import Path

class UpdateImage:
    
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
        entity: UpdateImageInput,
        file: tempfile.SpooledTemporaryFile | None = None,
        file_name: str | None = None,
        file_size: int | None = None,
        content_type: str | None = None,
    ) -> EpisodeImageModel:
        
        try:
            image_model: EpisodeImageModel = EpisodeImageModel.model_validate(entity, from_attributes=True)
            image: EpisodeImageModel = await self.episode_image_repo.get_by_id(entity.id)
            episode: EpisodeModel = await self.episode_repo.get_by_id(image.episode_id)
            pre_cover = image.cover
            if all([file, file_name, file_size, content_type]):
                try:
                    cover_name = secrets.token_hex(nbytes=5) + Path(file_name).suffix
                    result = await self.storage_repo.upload_object(
                        file,
                        f"{episode.id}/" + cover_name,
                        file_size,
                        content_type,
                    )      
                    if result:
                        image_model.cover = cover_name
                        image: EpisodeImageModel = await self.episode_image_repo.update(image_model)
                        await self.storage_repo.delete_object(f"{episode.id}/" + pre_cover)
                except:
                    image.cover = pre_cover
                    image: EpisodeImageModel = await self.episode_image_repo.update(image)
                    await self.storage_repo.delete_object(f"{episode.id}/" + cover_name)
            else:
                image: EpisodeImageModel = await self.episode_image_repo.update(image_model)

            return image
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  