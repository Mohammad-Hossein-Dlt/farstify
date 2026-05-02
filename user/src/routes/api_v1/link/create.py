from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.user.create_link_input import CreateLinkInput
from src.repo.interface.user.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.repo.interface.user.Iuser_link_repo import IUserLinkRepo
from src.routes.depends.repo_depend import user_link_repo_depend
from src.usecases.link.create import CreateLink
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create(
    entity: CreateLinkInput = Query(...),
    user_repo: IUserRepo = Depends(user_repo_depend),
    user_link_repo: IUserLinkRepo = Depends(user_link_repo_depend),
):
    try:
        create_link_usecase = CreateLink(user_repo, user_link_repo)
        output = await create_link_usecase.execute(entity)            
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
