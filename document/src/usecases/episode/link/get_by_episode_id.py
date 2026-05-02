from src.repo.interface.episode.Iepisode_link_repo import IEpisodeLinkRepo
from document.src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.domain.schemas.episode.episode_link import EpisodeLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllLinks:
    
    def __init__(
        self,
        episode_link_repo: IEpisodeLinkRepo,
    ):
        
        self.episode_link_repo = episode_link_repo
    
    async def execute(
        self,
        episode_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[EpisodeLinkModel]:
        
        try:
            links: list[BaseFilterCriteria] = await self.episode_link_repo.get_by_episode_id(episode_id, criteria)
            if isinstance(links, list):
                if criteria.order == "asc":
                    links.sort(key=lambda x: (x.order is None, x.order))
                elif criteria.order == "desc":
                    links.reverse()
                    links.sort(key=lambda x: (0 if x.order is None else 1, x.order), reverse=True)
            return links
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  