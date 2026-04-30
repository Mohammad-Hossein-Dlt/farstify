from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.interface.episode.Iepisode_image_repo import IEpisodeImageRepo
from src.repo.interface.episode.Iepisode_link_repo import IEpisodeLinkRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllEpisodes:
    
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
    ) -> OperationOutput:
        
        try:
            status = await self.storage_repo.clean_dir()
            if status:
                await self.episode_image_repo.delete_all()
                await self.episode_link_repo.delete_all()
                status = await self.episode_repo.delete_all()                    
            
            return OperationOutput(id=None, request="delete/all_episodes", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  