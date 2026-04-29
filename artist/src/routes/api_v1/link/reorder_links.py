from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.Iartist_link_repo import IArtistLinkRepo
from src.routes.depends.repo_depend import artist_link_repo_depend
from src.usecases.link.reorder_links import ReorderLinks
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/reorder",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def reorder_links(
    artist_id: str,
    link_ids: list[str],
    artist_link_repo: IArtistLinkRepo = Depends(artist_link_repo_depend),
):
    try:
        reorder_links_usecase = ReorderLinks(artist_link_repo)
        outputs_list = await reorder_links_usecase.execute(artist_id, link_ids)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
