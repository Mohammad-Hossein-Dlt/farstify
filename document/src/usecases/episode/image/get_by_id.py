from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.interface.episode.Iepisode_image_repo import IEpisodeImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.domain.schemas.episode.episode_image import EpisodeImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetImage:
    
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
    ) -> EpisodeImageModel:
        
        try:
            return await self.episode_image_repo.get_by_id(image_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  