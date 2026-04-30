from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.interface.episode.Iepisode_image_repo import IEpisodeImageRepo
from src.domain.schemas.episode.episode_image import EpisodeImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class ReorderImages:
    
    def __init__(
        self,
        episode_repo: IEpisodeRepo,
        episode_image_repo: IEpisodeImageRepo,
    ):
        
        self.episode_repo = episode_repo
        self.episode_image_repo = episode_image_repo
    
    async def execute(
        self,
        episode_id: str,
        image_ids: list[str],
    ) -> list[EpisodeImageModel]:
        
        try:
            images_list: list[EpisodeImageModel] = await self.episode_image_repo.get_by_episode_id(episode_id)
            for index, image_id in enumerate(image_ids):
                for image in images_list:
                    if str(image.id) == image_id:
                        image.order = index
                        await self.episode_image_repo.update(image)

            return await self.episode_image_repo.get_by_episode_id(episode_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  