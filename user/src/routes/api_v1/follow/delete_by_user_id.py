from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.follow.Ifollows_repo import IFollowsRepo
from src.routes.depends.repo_depend import follow_repo_depend
from src.usecases.follow.delete_by_user_id import DeleteAllFollows
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/all",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_by_user_id(
    user_id: str = Query(...),
    follow_repo: IFollowsRepo = Depends(follow_repo_depend),
):
    try:
        delete_all_follows_usecase = DeleteAllFollows(follow_repo)
        output = await delete_all_follows_usecase.execute(user_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
