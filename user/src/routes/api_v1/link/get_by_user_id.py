from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.repo.interface.user.Iuser_link_repo import IUserLinkRepo
from src.routes.depends.repo_depend import user_link_repo_depend
from src.usecases.link.get_by_user_id import GetAllLinks
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
    user_link_repo: IUserLinkRepo = Depends(user_link_repo_depend),
):
    try:
        get_all_links_usecase = GetAllLinks(user_link_repo)
        outputs_list = await get_all_links_usecase.execute(user_id, criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
