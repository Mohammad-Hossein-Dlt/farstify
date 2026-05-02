from ._router import router
from fastapi import UploadFile, Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.user.update_image_input import UpdateImageInput
from src.repo.interface.user.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.repo.interface.user.Iuser_image_repo import IUserImageRepo
from src.routes.depends.repo_depend import user_image_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.image.update import UpdateImage
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update(
    file: UploadFile | None = None,
    entity: UpdateImageInput = Query(...),
    user_repo: IUserRepo = Depends(user_repo_depend),
    user_image_repo: IUserImageRepo = Depends(user_image_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        
        update_image_usecase = UpdateImage(user_repo, user_image_repo, storage_repo)
        
        if file:
            output = await update_image_usecase.execute(
                entity,
                file.file,
                file.filename,
                file.size,
                file.content_type,
            )
        else:
            output = await update_image_usecase.execute(entity)
        
        return output.model_dump(mode="json")
    
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
