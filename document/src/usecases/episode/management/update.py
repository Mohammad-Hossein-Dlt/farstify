from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.episode.update_episode_input import UpdateEpisodeInput
from src.domain.schemas.episode.episode_model import EpisodeModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateEpisode:
    
    def __init__(
        self,
        episode_repo: IEpisodeRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.episode_repo = episode_repo  
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        entity: UpdateEpisodeInput,
    ) -> EpisodeModel:
        
        try:
            episode_model: EpisodeModel = EpisodeModel.model_validate(entity, from_attributes=True)
            return await self.episode_repo.update(episode_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")