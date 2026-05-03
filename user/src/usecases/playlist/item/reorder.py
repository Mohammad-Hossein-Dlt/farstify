from src.repo.interface.playlist.Iplaylist_item_repo import IPlaylistItemRepo
from src.domain.schemas.playlist.playlist_item_model import PlaylistItemModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class ReorderItems:
    
    def __init__(
        self,
        playlist_item_repo: IPlaylistItemRepo,
    ):
        
        self.playlist_item = playlist_item_repo
    
    async def execute(
        self,
        playlist_id: str,
        item_ids: list[str],
    ) -> list[PlaylistItemModel]:
        
        try:
            items_list: list[PlaylistItemModel] = await self.playlist_item.get_by_playlist_id(playlist_id)
            for index, item_id in enumerate(item_ids):
                for item in items_list:
                    if str(item.id) == item_id:
                        item.order = index
                        await self.playlist_item.update(item)

            return await self.playlist_item.get_by_playlist_id(playlist_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  