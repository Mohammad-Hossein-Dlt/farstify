from src.repo.interface.episode.Iepisode_link_repo import IEpisodeLinkRepo
from src.domain.schemas.episode.episode_link import EpisodeLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class ReorderLinks:
    
    def __init__(
        self,
        episode_link_repo: IEpisodeLinkRepo,
    ):

        self.episode_link_repo = episode_link_repo
    
    async def execute(
        self,
        episode_id: str,
        link_ids: list[str],
    ) -> list[EpisodeLinkModel]:
        
        try:
            links_list: list[EpisodeLinkModel] = await self.episode_link_repo.get_by_episode_id(episode_id)
            for index, links_id in enumerate(link_ids):
                for link in links_list:
                    if str(link.id) == links_id:
                        link.order = index
                        await self.episode_link_repo.update(link)

            return await self.episode_link_repo.get_by_episode_id(episode_id)        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  