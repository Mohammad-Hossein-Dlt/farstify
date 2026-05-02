from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.follow.Ifollow_repo import IFollowRepo
from src.routes.depends.repo_depend import follow_repo_depend
from src.usecases.follow.delete_by_id import DeleteFollow
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_by_id(
    target_id: str = Query(...),
    follow_repo: IFollowRepo = Depends(follow_repo_depend),
):
    try:
        delete_follow_usecase = DeleteFollow(follow_repo)
        output = await delete_follow_usecase.execute(target_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
