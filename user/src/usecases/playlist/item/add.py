from src.repo.interface.playlist.Iplaylist_item_repo import IPlaylistItemRepo
from src.models.schemas.playlist.add_playlist_item_input import AddPlaylistItemInput
from src.domain.schemas.playlist.playlist_item_model import PlaylistItemModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class AddItem:
    
    def __init__(
        self,
        playlist_item_repo: IPlaylistItemRepo,
    ):
        
        self.playlist_item_repo = playlist_item_repo
    
    async def execute(
        self,
        entity: AddPlaylistItemInput,
    ) -> PlaylistItemModel:
        
        try:
            item_model: PlaylistItemModel = PlaylistItemModel.model_validate(entity, from_attributes=True)
            return await self.playlist_item_repo.create(item_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  