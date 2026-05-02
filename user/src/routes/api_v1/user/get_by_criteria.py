from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from user.src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.usecases.user.get_by_criteria import GetAllUsers
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_by_criteria(
    criteria: BaseFilterCriteria = Query(...),
    user_repo: IUserRepo = Depends(user_repo_depend),
):
    try:
        get_all_users_usecase = GetAllUsers(user_repo)
        outputs_list = await get_all_users_usecase.execute(criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
