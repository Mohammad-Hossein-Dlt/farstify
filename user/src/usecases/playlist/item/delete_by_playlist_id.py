from src.repo.interface.playlist.Iplaylist_item_repo import IPlaylistItemRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteItems:
    
    def __init__(
        self,
        playlist_item_repo: IPlaylistItemRepo,
    ):
        
        self.playlist_repo = playlist_item_repo
    
    async def execute(
        self,
        playlist_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.playlist_repo.delete_by_playlist_id(playlist_id)            
            return OperationOutput(id=playlist_id, request="delete/playlist-items", status=status)        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  