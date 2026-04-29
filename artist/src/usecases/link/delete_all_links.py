from src.repo.interface.Iartist_link_repo import IArtistLinkRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllLinks:
    
    def __init__(
        self,
        artist_link_repo: IArtistLinkRepo,
    ):
        
        self.artist_link_repo = artist_link_repo
    
    async def execute(
        self,
        artist_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.artist_link_repo.delete_artist_links(artist_id)
            return OperationOutput(id=artist_id, request="delete/all-artist-links", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  