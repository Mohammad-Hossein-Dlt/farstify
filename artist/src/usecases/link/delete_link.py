from src.repo.interface.Iartist_link_repo import IArtistLinkRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteLink:
    
    def __init__(
        self,
        artist_link_repo: IArtistLinkRepo,
    ):
        
        self.artist_link_repo = artist_link_repo
    
    async def execute(
        self,
        link_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.artist_link_repo.delete_link(link_id)
            return OperationOutput(id=link_id, request="delete/artist-link", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  