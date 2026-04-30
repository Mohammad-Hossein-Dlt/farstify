from src.repo.interface.episode.Iepisode_link_repo import IEpisodeLinkRepo
from src.domain.schemas.episode.episode_link import EpisodeLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetLink:
    
    def __init__(
        self,
        episode_link_repo: IEpisodeLinkRepo,
    ):
        
        self.episode_link_repo = episode_link_repo
    
    async def execute(
        self,
        link_id: str,
    ) -> EpisodeLinkModel:
        
        try:
            return await self.episode_link_repo.get_by_id(link_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  