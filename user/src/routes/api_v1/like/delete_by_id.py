from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.like.Ilikes_repo import ILikesRepo
from src.routes.depends.repo_depend import like_repo_depend
from src.usecases.like.delete_by_id import DeleteLike
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
    like_repo: ILikesRepo = Depends(like_repo_depend),
):
    try:
        delete_like_usecase = DeleteLike(like_repo)
        output = await delete_like_usecase.execute(target_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
