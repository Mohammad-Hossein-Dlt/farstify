from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.repo.interface.follow.Ifollows_repo import IFollowsRepo
from src.routes.depends.repo_depend import follow_repo_depend
from src.usecases.follow.get_by_user_id import GetAllFollows
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
    follow_repo: IFollowsRepo = Depends(follow_repo_depend),
):
    try:
        get_all_follows_usecase = GetAllFollows(follow_repo)
        outputs_list = await get_all_follows_usecase.execute(user_id, criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
