from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.playlist.add_playlist_item_input import AddPlaylistItemInput
from src.repo.interface.playlist.Iplaylist_item_repo import IPlaylistItemRepo
from src.routes.depends.repo_depend import playlist_item_repo_depend
from src.usecases.playlist.item.add import AddItem
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def add_item(
    entity: AddPlaylistItemInput = Query(...),
    playlist_item_repo: IPlaylistItemRepo = Depends(playlist_item_repo_depend),
):
    try:
        add_playlist_item_usecase = AddItem(playlist_item_repo)
        output = await add_playlist_item_usecase.execute(entity)            
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
