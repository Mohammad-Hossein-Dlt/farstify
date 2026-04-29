from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
from src.usecases.category.get_all_categories import GetAllCategories
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.routes.depends.repo_depend import category_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_all_categories(
    filter: CategoryFilterInput = Query(...),
    category_repo: ICategoryRepo = Depends(category_repo_depend),
):
    try:
        get_all_categoryies_usecase = GetAllCategories(category_repo)
        outputs_list = await get_all_categoryies_usecase.execute(filter)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
