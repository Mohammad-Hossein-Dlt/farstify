from src.repo.interface.user.Iuser_repo import IUserRepo
from src.repo.interface.playlist.Iplaylist_repo import IPlaylistRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.playlist.update_playlist_input import UpdatePlaylistInput
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.playlist.playlist_model import PlaylistModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
import tempfile
import secrets
from pathlib import Path

class UpdatePlaylist:
    
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
        entity: UpdatePlaylistInput,
        file: tempfile.SpooledTemporaryFile | None = None,
        file_name: str | None = None,
        file_size: int | None = None,
        content_type: str | None = None,
    ) -> PlaylistModel:
        
        try:
            playlist_model: PlaylistModel = PlaylistModel.model_validate(entity, from_attributes=True)
            playlist: PlaylistModel = await self.playlist_repo.get_by_id(entity.id)
            user: UserModel = await self.user_repo.get_by_id(playlist.user_id)
            prev_cover = playlist.cover
            if all([file, file_name, file_size, content_type]):
                cover_name = secrets.token_hex(nbytes=5) + Path(file_name).suffix
                base_path = f"{user.id}/playlist/{playlist.id}/image"
                new_object_name = f"{base_path}/{cover_name}"
                prev_object_name = f"{base_path}/{prev_cover}"
                try:
                    result = await self.storage_repo.upload_object(
                        file,
                        new_object_name,
                        file_size,
                        content_type,
                    )      
                    if result:
                        playlist_model.cover = cover_name
                        playlist: PlaylistModel = await self.playlist_repo.update(playlist_model)
                        await self.storage_repo.delete_object(prev_object_name)
                except:
                    playlist.cover = prev_cover
                    playlist: PlaylistModel = await self.playlist_repo.update(playlist)
                    await self.storage_repo.delete_object(new_object_name)
            else:
                playlist: PlaylistModel = await self.playlist_repo.update(playlist_model)

            return playlist
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  