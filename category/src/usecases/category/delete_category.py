from src.repo.interface.Icategory_repo import ICategoryRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.exceptions.exceptions import AppBaseException, Error, OperationFailureException

class DeleteCategory:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.category_repo = category_repo   
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        category_id: str,
    ) -> OperationOutput:
        
        try:
            
            category: CategoryModel = await self.category_repo.get_category_by_id(category_id)
            
            if category.cover:
                delete_cover = await self.storage_repo.delete_object(category.cover)
                if not delete_cover:
                    raise Error(500, "Can't delete the cover of the category")
                            
            status = await self.category_repo.delete_category(category_id)
            
            return OperationOutput(id=category_id, request="delete/category", status=status)
        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  