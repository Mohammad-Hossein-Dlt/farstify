from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.interface.episode.Iepisode_image_repo import IEpisodeImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.domain.schemas.episode.episode_model import EpisodeModel
from src.domain.schemas.episode.episode_image import EpisodeImageModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteImage:
    
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
        image_id: str,
    ) -> OperationOutput:
        
        try:
            
            image: EpisodeImageModel = await self.episode_image_repo.get_by_id(image_id)
            episode: EpisodeModel = await self.episode_repo.get_by_id(image.episode_id)
            
            result = await self.storage_repo.delete_object(f"{episode.id}/" + image.cover)
            
            status = False
            if result:
                status = await self.episode_image_repo.delete_by_id(image.id)

            return OperationOutput(id=image_id, request="delete/episode-image", status=status)
        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  