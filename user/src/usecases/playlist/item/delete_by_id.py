from src.repo.interface.playlist.Iplaylist_item_repo import IPlaylistItemRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteItem:
    
    def __init__(
        self,
        playlist_item_repo: IPlaylistItemRepo,
    ):
        
        self.playlist_item_repo = playlist_item_repo
    
    async def execute(
        self,
        item_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.playlist_item_repo.delete_by_id(item_id)
            return OperationOutput(id=item_id, request="delete/playlist-item", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  