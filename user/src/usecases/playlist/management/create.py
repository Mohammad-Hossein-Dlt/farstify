from src.repo.interface.user.Iuser_repo import IUserRepo
from src.repo.interface.playlist.Iplaylist_repo import IPlaylistRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.playlist.create_playlist_input import CreatePlaylistInput
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.playlist.playlist_model import PlaylistModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
from pathlib import Path
import tempfile
import secrets

class CreatePlaylist:
    
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
        entity: CreatePlaylistInput,
        file: tempfile.SpooledTemporaryFile | None = None,
        file_name: str | None = None,
        file_size: int | None = None,
        content_type: str | None = None,
    ) -> PlaylistModel:
        
        try:
            playlist_model: PlaylistModel = PlaylistModel.model_validate(entity, from_attributes=True)
            user: UserModel = await self.user_repo.get_by_id(entity.user_id)
            playlist: PlaylistModel = await self.playlist_repo.create(playlist_model)
            if all([file, file_name, file_size, content_type]):
                cover_name = secrets.token_hex(nbytes=5) + Path(file_name).suffix
                base_path = f"{user.id}/playlist/{playlist.id}/image"
                new_object_name = f"{base_path}/{cover_name}"
                try:
                    result = await self.storage_repo.upload_object(
                        file,
                        new_object_name,
                        file_size,
                        content_type,
                    )
                    if result:
                        playlist.cover = cover_name
                        playlist: PlaylistModel = await self.playlist_repo.update(playlist)
                except:
                    if playlist.id:
                        await self.playlist_repo.delete_by_id(playlist.id)
                    await self.storage_repo.delete_object(new_object_name)

            return playlist
                        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  