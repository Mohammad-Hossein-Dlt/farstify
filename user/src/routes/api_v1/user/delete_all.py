from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.user.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.repo.interface.user.Iuser_image_repo import IUserImageRepo
from src.routes.depends.repo_depend import user_image_repo_depend
from src.repo.interface.user.Iuser_link_repo import IUserLinkRepo
from src.routes.depends.repo_depend import user_link_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.user.delete_all import DeleteAllUsers
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/all",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_all(
    user_repo: IUserRepo = Depends(user_repo_depend),
    user_image_repo: IUserImageRepo = Depends(user_image_repo_depend),
    user_link_repo: IUserLinkRepo = Depends(user_link_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        delete_all_users_usecase = DeleteAllUsers(user_repo, user_image_repo, user_link_repo, storage_repo)
        output = await delete_all_users_usecase.execute()
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
