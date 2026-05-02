from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.interface.episode.Iepisode_image_repo import IEpisodeImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from document.src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.domain.schemas.episode.episode_image import EpisodeImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllImages:
    
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
        episode_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[EpisodeImageModel]:
        
        try:
            images: list[EpisodeImageModel] = await self.episode_image_repo.get_by_episode_id(episode_id, criteria)
            if isinstance(images, list):
                if criteria.order == "asc":
                    images.sort(key=lambda x: (x.order is None, x.order))
                elif criteria.order == "desc":
                    images.reverse()
                    images.sort(key=lambda x: (0 if x.order is None else 1, x.order), reverse=True)
            return images
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  