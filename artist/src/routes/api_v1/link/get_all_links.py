from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.sort_direction_filter_input import SortDirectionFilterInput
from src.repo.interface.Iartist_link_repo import IArtistLinkRepo
from src.routes.depends.repo_depend import artist_link_repo_depend
from src.usecases.link.get_all_links import GetAllLinks
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_all_links(
    to_filter: SortDirectionFilterInput = Query(...),
    artist_link_repo: IArtistLinkRepo = Depends(artist_link_repo_depend),
):
    try:
        get_all_links_usecase = GetAllLinks(artist_link_repo)
        outputs_list = await get_all_links_usecase.execute(to_filter)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
