from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.like.Ilikes_repo import ILikesRepo
from src.routes.depends.repo_depend import like_repo_depend
from src.usecases.like.get_by_id import GetLike
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
    like_repo: ILikesRepo = Depends(like_repo_depend),
):
    try:
        get_like_usecase = GetLike(like_repo)
        output = await get_like_usecase.execute(target_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
