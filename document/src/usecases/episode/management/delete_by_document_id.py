from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.interface.episode.Iepisode_image_repo import IEpisodeImageRepo
from src.repo.interface.episode.Iepisode_link_repo import IEpisodeLinkRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.domain.schemas.episode.episode_model import EpisodeModel
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
        document_id: str,
    ) -> OperationOutput:
        
        try:
            episodes_list: list[EpisodeModel] = await self.episode_repo.get_by_document_id(document_id)
            
            status = True if episodes_list else False
            for episode in episodes_list:
                result = await self.storage_repo.delete_objects(f"{episode.document_id}/{episode.id}")
                if result:
                    await self.episode_repo.delete_by_id(episode.id)
                else:
                    status = False
                    
            return OperationOutput(id=None, request="delete/all_episodes", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  