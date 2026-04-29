from src.repo.interface.Iartist_link_repo import IArtistLinkRepo
from src.domain.schemas.artist.artist_link import ArtistLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetLink:
    
    def __init__(
        self,
        artist_link_repo: IArtistLinkRepo,
    ):
        
        self.artist_link_repo = artist_link_repo
    
    async def execute(
        self,
        link_id: str,
    ) -> ArtistLinkModel:
        
        try:
            return await self.artist_link_repo.get_link_by_id(link_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  