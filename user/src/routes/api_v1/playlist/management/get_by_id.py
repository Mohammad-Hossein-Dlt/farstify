from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.user.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.repo.interface.playlist.Iplaylist_repo import IPlaylistRepo
from src.routes.depends.repo_depend import playlist_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.playlist.management.get_by_id import GetPlaylist
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_by_id(
    playlist_id: str = Query(...),
    user_repo: IUserRepo = Depends(user_repo_depend),
    playlist_repo: IPlaylistRepo = Depends(playlist_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        get_playlist_usecase = GetPlaylist(user_repo, playlist_repo, storage_repo)
        output = await get_playlist_usecase.execute(playlist_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
