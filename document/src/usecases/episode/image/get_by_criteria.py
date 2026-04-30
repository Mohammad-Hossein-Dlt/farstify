from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.interface.episode.Iepisode_image_repo import IEpisodeImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.filter.sort_direction_filter_input import SortDirectionFilterInput
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
        criteria: SortDirectionFilterInput,
    ) -> list[EpisodeImageModel]:
        
        try:
            images: list[EpisodeImageModel] = await self.episode_image_repo.get_by_episode_id(criteria.value)
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