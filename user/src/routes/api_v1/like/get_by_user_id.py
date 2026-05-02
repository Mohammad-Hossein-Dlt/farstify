from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.repo.interface.like.Ilikes_repo import ILikesRepo
from src.routes.depends.repo_depend import like_repo_depend
from src.usecases.like.get_by_user_id import GetAllLikes
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
    like_repo: ILikesRepo = Depends(like_repo_depend),
):
    try:
        get_all_likes_usecase = GetAllLikes(like_repo)
        outputs_list = await get_all_likes_usecase.execute(user_id, criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
