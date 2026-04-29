from src.repo.interface.Icategory_repo import ICategoryRepo
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllCategories:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
    ):
        
        self.category_repo = category_repo  
    
    async def execute(
        self,
        filter: CategoryFilterInput,
    ) -> list[CategoryModel]:
        
        try:
            return await self.category_repo.get_categories_with_filter(filter)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  