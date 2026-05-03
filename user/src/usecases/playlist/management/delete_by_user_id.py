from src.repo.interface.user.Iuser_repo import IUserRepo
from src.repo.interface.playlist.Iplaylist_repo import IPlaylistRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.playlist.playlist_model import PlaylistModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeletePlaylists:
    
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
        user_id: str,
    ) -> OperationOutput:
        
        try:
            user: UserModel = await self.user_repo.get_by_id(user_id)
            playlists: list[PlaylistModel] = await self.playlist_repo.get_by_user_id(user_id)
            
            status = True if playlists else False
            for p in playlists:
                result = await self.storage_repo.delete_object(f"{user.id}/playlist/{p.id}/image/{p.cover}")
                if result:
                    await self.playlist_repo.delete_by_id(p.id)
                else:
                    status = False
            
            return OperationOutput(id=user_id, request="delete/all-user-playlists", status=status)        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  