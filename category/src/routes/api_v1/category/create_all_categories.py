from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.routes.depends.repo_depend import category_repo_depend
from src.usecases.category.create_all_categories import CreateAllCategory
from data.categories import all_categories
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/all",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create_category(
    category_repo: ICategoryRepo = Depends(category_repo_depend),
):
    try:
        create_category_usecase = CreateAllCategory(category_repo)
        output = await create_category_usecase.execute(all_categories)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
