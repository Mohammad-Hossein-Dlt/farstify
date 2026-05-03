from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.playlist.Iplaylist_item_repo import IPlaylistItemRepo
from src.routes.depends.repo_depend import playlist_item_repo_depend
from src.usecases.playlist.item.delete_by_id import DeleteItem
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_by_id(
    item_id: str = Query(...),
    playlist_item_repo: IPlaylistItemRepo = Depends(playlist_item_repo_depend),
):
    try:
        delete_playlist_item_usecase = DeleteItem(playlist_item_repo)
        output = await delete_playlist_item_usecase.execute(item_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
