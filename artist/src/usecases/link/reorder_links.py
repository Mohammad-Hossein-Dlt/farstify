from src.repo.interface.Iartist_link_repo import IArtistLinkRepo
from src.domain.schemas.artist.artist_link import ArtistLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class ReorderLinks:
    
    def __init__(
        self,
        artist_link_repo: IArtistLinkRepo,
    ):

        self.artist_link_repo = artist_link_repo
    
    async def execute(
        self,
        artist_id: str,
        link_ids: list[str],
    ) -> ArtistLinkModel:
        
        try:
            links_list: list[ArtistLinkModel] = await self.artist_link_repo.get_links(artist_id)
            for index, links_id in enumerate(link_ids):
                for link in links_list:
                    if str(link.id) == links_id:
                        link.order = index
                        await self.artist_link_repo.update_link(link)

            return await self.artist_link_repo.get_links(artist_id)        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  