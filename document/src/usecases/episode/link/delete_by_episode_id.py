from src.repo.interface.episode.Iepisode_link_repo import IEpisodeLinkRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllLinks:
    
    def __init__(
        self,
        episode_link_repo: IEpisodeLinkRepo,
    ):
        
        self.episode_link_repo = episode_link_repo
    
    async def execute(
        self,
        episode_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.episode_link_repo.delete_by_episode_id(episode_id)
            return OperationOutput(id=episode_id, request="delete/all-episode-links", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  