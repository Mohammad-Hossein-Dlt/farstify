from src.repo.interface.episode.Iepisode_link_repo import IEpisodeLinkRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteLink:
    
    def __init__(
        self,
        episode_link_repo: IEpisodeLinkRepo,
    ):
        
        self.episode_link_repo = episode_link_repo
    
    async def execute(
        self,
        link_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.episode_link_repo.delete_by_id(link_id)
            return OperationOutput(id=link_id, request="delete/episode-link", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  