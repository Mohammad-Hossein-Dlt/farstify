from ._router import router
from fastapi import UploadFile, Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.playlist.create_playlist_input import CreatePlaylistInput
from src.repo.interface.user.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.repo.interface.playlist.Iplaylist_repo import IPlaylistRepo
from src.routes.depends.repo_depend import playlist_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.playlist.management.create import CreatePlaylist
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create(
    file: UploadFile | None = None,
    entity: CreatePlaylistInput = Query(...),
    user_repo: IUserRepo = Depends(user_repo_depend),
    playlist_repo: IPlaylistRepo = Depends(playlist_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        
        create_playlist_usecase = CreatePlaylist(user_repo, playlist_repo, storage_repo)
        
        if file:
            output = await create_playlist_usecase.execute(
                entity,
                file.file,
                file.filename,
                file.size,
                file.content_type,
            )
        else:
            output = await create_playlist_usecase.execute(entity)
            
        return output.model_dump(mode="json")
    
    except AppBaseException as ex:
        raise
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
