from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.models.schemas.filter.sort_direction_filter_input import SortDirectionFilterInput
from src.domain.schemas.episode.episode_model import EpisodeModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllEpisodes:
    
    def __init__(
        self,
        episode_repo: IEpisodeRepo,
    ):
        
        self.episode_repo = episode_repo  
    
    async def execute(
        self,
        criteria: SortDirectionFilterInput,
    ) -> list[EpisodeModel]:
        
        try:
            episodes: list[EpisodeModel] = await self.episode_repo.get_by_document_id(criteria.value)
            if isinstance(episodes, list):
                if criteria.order == "asc":
                    pass
                elif criteria.order == "desc":
                    episodes.reverse()
            return episodes
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  