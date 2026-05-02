from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.follow.Ifollow_repo import IFollowRepo
from src.routes.depends.repo_depend import follow_repo_depend
from src.usecases.follow.get_by_id import GetFollow
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_by_id(
    target_id: str = Query(...),
    follow_repo: IFollowRepo = Depends(follow_repo_depend),
):
    try:
        get_follow_usecase = GetFollow(follow_repo)
        output = await get_follow_usecase.execute(target_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
