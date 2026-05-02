from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.follow.Ifollow_repo import IFollowRepo
from src.routes.depends.repo_depend import follow_repo_depend
from src.usecases.follow.create_all import CreateAllFollow
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/all",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create_all(
    follow_repo: IFollowRepo = Depends(follow_repo_depend),
):
    try:
        create_follow_usecase = CreateAllFollow(follow_repo)
        output = await create_follow_usecase.execute()            
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
