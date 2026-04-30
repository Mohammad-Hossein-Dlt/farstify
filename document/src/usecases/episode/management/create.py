from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.episode.create_episode_input import CreateEpisodeInput
from src.domain.schemas.episode.episode_model import EpisodeModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateEpisode:
    
    def __init__(
        self,
        episode_repo: IEpisodeRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.episode_repo = episode_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        entity: CreateEpisodeInput,
    ) -> EpisodeModel:
        
        try:
            episode_model: EpisodeModel = EpisodeModel.model_validate(entity, from_attributes=True)
            return await self.episode_repo.create(episode_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  