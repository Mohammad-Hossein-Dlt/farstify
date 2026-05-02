from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.like.like_input import LikeInput
from src.repo.interface.like.Ilikes_repo import ILikesRepo
from src.routes.depends.repo_depend import like_repo_depend
from src.usecases.like.create import CreateLike
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create(
    entity: LikeInput = Query(...),
    like_repo: ILikesRepo = Depends(like_repo_depend),
):
    try:
        create_like_usecase = CreateLike(like_repo)
        output = await create_like_usecase.execute(entity)            
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
