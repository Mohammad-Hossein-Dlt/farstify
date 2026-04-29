from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.routes.depends.repo_depend import category_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.category.delete_category import DeleteCategory
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_category(
    category_id: str = Query(...),
    category_repo: ICategoryRepo = Depends(category_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        delete_category_usecase = DeleteCategory(category_repo, storage_repo)
        output = await delete_category_usecase.execute(category_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
