from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.domain.schemas.episode.episode_model import EpisodeModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetEpisode:
    
    def __init__(
        self,
        episode_repo: IEpisodeRepo,
    ):
        
        self.episode_repo = episode_repo  
    
    async def execute(
        self,
        episode_id: str,
    ) -> EpisodeModel:
        
        try:
            return await self.episode_repo.get_by_id(episode_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")