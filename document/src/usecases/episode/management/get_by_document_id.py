from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
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
        document_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[EpisodeModel]:
        
        try:
            return await self.episode_repo.get_by_document_id(document_id, criteria)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  