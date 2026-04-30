from ._router import router
from fastapi import UploadFile, Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.category.create_category_input import CreateCategoryInput
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.routes.depends.repo_depend import category_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.category.create import CreateCategory
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create(
    file: UploadFile | None = None,
    entity: CreateCategoryInput = Query(...),
    category_repo: ICategoryRepo = Depends(category_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        
        create_category_usecase = CreateCategory(category_repo, storage_repo)
        
        if file:
            output = await create_category_usecase.execute(
                entity,
                file.file,
                file.filename,
                file.size,
                file.content_type,
            )
        else:
            output = await create_category_usecase.execute(entity)
            
        return output.model_dump(mode="json")
    
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
