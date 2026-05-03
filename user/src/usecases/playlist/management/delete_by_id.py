from src.repo.interface.user.Iuser_repo import IUserRepo
from src.repo.interface.playlist.Iplaylist_repo import IPlaylistRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.playlist.playlist_model import PlaylistModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeletePlaylist:
    
    def __init__(
        self,
        user_repo: IUserRepo,
        playlist_repo: IPlaylistRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.user_repo = user_repo
        self.playlist_repo = playlist_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        playlist_id: str,
    ) -> OperationOutput:
        
        try:
            
            playlist: PlaylistModel = await self.playlist_repo.get_by_id(playlist_id)
            user: UserModel = await self.user_repo.get_by_id(playlist.user_id)
            
            result = await self.storage_repo.delete_object(f"{user.id}/playlist/{playlist.id}/image/{playlist.cover}")
            
            status = False
            if result:
                status = await self.playlist_repo.delete_by_id(playlist.id)

            return OperationOutput(id=playlist_id, request="delete/user-playlist", status=status)
        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  