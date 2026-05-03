from src.repo.interface.playlist.Iplaylist_item_repo import IPlaylistItemRepo
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.domain.schemas.playlist.playlist_item_model import PlaylistItemModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetItems:
    
    def __init__(
        self,
        playlist_item_repo: IPlaylistItemRepo,
    ):
        
        self.playlist_item_repo = playlist_item_repo
    
    async def execute(
        self,
        playlist_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[PlaylistItemModel]:
        
        try:
            return await self.playlist_item_repo.get_by_playlist_id(playlist_id, criteria)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  