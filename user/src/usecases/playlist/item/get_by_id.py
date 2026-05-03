from src.repo.interface.playlist.Iplaylist_item_repo import IPlaylistItemRepo
from src.domain.schemas.playlist.playlist_item_model import PlaylistItemModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetItem:
    
    def __init__(
        self,
        playlist_item_repo: IPlaylistItemRepo,
    ):
        
        self.playlist_item_repo = playlist_item_repo
    
    async def execute(
        self,
        item_id: str,
    ) -> PlaylistItemModel:
        
        try:
            return await self.playlist_item_repo.get_by_id(item_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  