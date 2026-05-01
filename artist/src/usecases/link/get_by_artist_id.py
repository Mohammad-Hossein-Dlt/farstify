from src.repo.interface.Iartist_link_repo import IArtistLinkRepo
from src.models.schemas.filter.sort_direction_filter_input import SortDirectionFilterInput
from src.domain.schemas.artist.artist_link import ArtistLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllLinks:
    
    def __init__(
        self,
        artist_link_repo: IArtistLinkRepo,
    ):
        
        self.artist_link_repo = artist_link_repo
    
    async def execute(
        self,
        criteria: SortDirectionFilterInput,
    ) -> list[ArtistLinkModel]:
        
        try:
            links: list[SortDirectionFilterInput] = await self.artist_link_repo.get_by_artist_id(criteria.value)
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