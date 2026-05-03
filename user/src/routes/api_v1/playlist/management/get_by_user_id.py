from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.repo.interface.user.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.repo.interface.playlist.Iplaylist_repo import IPlaylistRepo
from src.routes.depends.repo_depend import playlist_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.playlist.management.get_by_user_id import GetPlaylists
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_by_user_id(
    user_id: str = Query(...),
    criteria: BaseFilterCriteria = Depends(),
    user_repo: IUserRepo = Depends(user_repo_depend),
    playlist_repo: IPlaylistRepo = Depends(playlist_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        get_playlists_usecase = GetPlaylists(user_repo, playlist_repo, storage_repo)
        outputs_list = await get_playlists_usecase.execute(user_id, criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
