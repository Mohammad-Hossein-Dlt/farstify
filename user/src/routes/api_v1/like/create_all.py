from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.like.Ilikes_repo import ILikesRepo
from src.routes.depends.repo_depend import like_repo_depend
from src.usecases.like.create_all import CreateAllLike
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/all",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create_all(
    like_repo: ILikesRepo = Depends(like_repo_depend),
):
    try:
        create_like_usecase = CreateAllLike(like_repo)
        output = await create_like_usecase.execute()            
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
