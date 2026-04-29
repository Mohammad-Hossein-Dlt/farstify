from src.repo.interface.Icategory_repo import ICategoryRepo
from src.models.schemas.category.create_category_input import CreateCategoryInput
from src.domain.schemas.category.category_model import CategoryModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, EntityNotFoundError, OperationFailureException

class CreateAllCategory:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
    ):
        
        self.category_repo = category_repo
    
    async def execute(
        self,
        categories: list[CreateCategoryInput],
    ) -> CategoryModel:
        
        for category in categories:
        
            if category.parent_id:
                try:
                    parent: CategoryModel = await self.category_repo.get_category_by_id(category.parent_id)
                    category.parent_id = parent.id
                except EntityNotFoundError as ex:
                    raise EntityNotFoundError(ex.status_code, "Parent not found")
            
            try:
                category = CategoryModel.model_validate(category, from_attributes=True)
                await self.category_repo.create_category(category)
            except AppBaseException:
                raise
            except:
                raise OperationFailureException(500, "Internal server error")
            
        return OperationOutput(id=None, request="create/all-categories", status=True)