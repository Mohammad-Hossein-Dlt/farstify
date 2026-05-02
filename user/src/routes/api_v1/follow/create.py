from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.user.create_follow_input import CreateFollowInput
from src.repo.interface.follow.Ifollow_repo import IFollowRepo
from src.routes.depends.repo_depend import follow_repo_depend
from src.usecases.follow.create import CreateFollow
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create(
    entity: CreateFollowInput = Query(...),
    follow_repo: IFollowRepo = Depends(follow_repo_depend),
):
    try:
        create_follow_usecase = CreateFollow(follow_repo)
        output = await create_follow_usecase.execute(entity)            
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
