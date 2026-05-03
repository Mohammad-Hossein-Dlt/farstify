from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.playlist.Iplaylist_item_repo import IPlaylistItemRepo
from src.routes.depends.repo_depend import playlist_item_repo_depend
from src.usecases.playlist.item.reorder import ReorderItems
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/reorder",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def reorder(
    playlist_id: str,
    item_ids: list[str],
    playlist_item_repo: IPlaylistItemRepo = Depends(playlist_item_repo_depend),
):
    try:
        reorder_items_usecase = ReorderItems(playlist_item_repo)
        outputs_list = await reorder_items_usecase.execute(playlist_id, item_ids)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
