from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.interface.episode.Iepisode_image_repo import IEpisodeImageRepo
from src.repo.interface.episode.Iepisode_link_repo import IEpisodeLinkRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.domain.schemas.episode.episode_model import EpisodeModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteEpisode:
    
    def __init__(
        self,
        episode_repo: IEpisodeRepo,
        episode_image_repo: IEpisodeImageRepo,
        episode_link_repo: IEpisodeLinkRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.episode_repo = episode_repo
        self.episode_image_repo = episode_image_repo
        self.episode_link_repo = episode_link_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        episode_id: str,
    ) -> OperationOutput:
        
        try:
            status = False
            episode: EpisodeModel = await self.episode_repo.get_by_id(episode_id)
            check_path = await self.storage_repo.path_objects(str(episode.id))
            if check_path:
                delete_objects = await self.storage_repo.delete_objects(str(episode.id))
                if delete_objects:
                    await self.episode_image_repo.delete_by_episode_id(episode_id)
                    await self.episode_link_repo.delete_by_episode_id(episode_id)
                    status = await self.episode_repo.delete_by_id(episode_id)
            else:
                await self.episode_image_repo.delete_by_episode_id(episode_id)
                await self.episode_link_repo.delete_by_episode_id(episode_id)
                status = await self.episode_repo.delete_by_id(episode_id)
            
            return OperationOutput(id=episode_id, request="delete/episode", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  