from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.user.Iuser_link_repo import IUserLinkRepo
from src.routes.depends.repo_depend import user_link_repo_depend
from src.usecases.link.delete_by_user_id import DeleteAllLinks
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
    user_link_repo: IUserLinkRepo = Depends(user_link_repo_depend),
):
    try:
        delete_all_links_usecase = DeleteAllLinks(user_link_repo)
        output = await delete_all_links_usecase.execute(user_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
