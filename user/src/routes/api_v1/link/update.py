from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.user.update_link_input import UpdateLinkInput
from src.repo.interface.Iuser_link_repo import IUserLinkRepo
from src.routes.depends.repo_depend import user_link_repo_depend
from src.usecases.link.update import UpdateLink
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update(
    entity: UpdateLinkInput = Query(...),
    user_link_repo: IUserLinkRepo = Depends(user_link_repo_depend),
):
    try:
        update_link_usecase = UpdateLink(user_link_repo)
        output = await update_link_usecase.execute(entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
