from src.repo.interface.user.Iuser_repo import IUserRepo
from src.repo.interface.playlist.Iplaylist_repo import IPlaylistRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.domain.schemas.playlist.playlist_model import PlaylistModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetPlaylists:
    
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
        criteria: BaseFilterCriteria,
    ) -> list[PlaylistModel]:
        
        try:
            return await self.playlist_repo.get_by_user_id(user_id, criteria)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  