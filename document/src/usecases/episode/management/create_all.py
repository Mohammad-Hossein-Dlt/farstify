from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.models.schemas.episode.create_episode_input import CreateEpisodeInput
from src.domain.schemas.episode.episode_model import EpisodeModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateAllEpisodes:
    
    def __init__(
        self,
        episode_repo: IEpisodeRepo,
    ):
        
        self.episode_repo = episode_repo
    
    async def execute(
        self,
        episodes: list[CreateEpisodeInput],
    ) -> EpisodeModel:
        
        for episode in episodes:
            
            try:
                episode_model = EpisodeModel.model_validate(episode, from_attributes=True)
                await self.episode_repo.create(episode_model)
            except AppBaseException:
                raise
            except:
                raise OperationFailureException(500, "Internal server error")
            
        return OperationOutput(id=None, request="create/all_episodes", status=True)