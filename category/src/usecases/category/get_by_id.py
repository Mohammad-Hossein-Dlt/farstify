from src.repo.interface.Icategory_repo import ICategoryRepo
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetCategory:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
    ):
        
        self.category_repo = category_repo  
    
    async def execute(
        self,
        category_id: str,
    ) -> CategoryModel:
        
        try:
            return await self.category_repo.get_by_id(category_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")