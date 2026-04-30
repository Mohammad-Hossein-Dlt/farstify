from src.repo.interface.Icategory_repo import ICategoryRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllCategoriesByParentId:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
        storage_repo: IStorageRepo,
    ):        
        
        self.category_repo = category_repo   
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        parent_id: str,
    ) -> OperationOutput:
        
        try:
            categories: list[CategoryModel] = await self.category_repo.get_descendants(parent_id)
            status = True if categories else False
            for c in categories:
                result = True
                if c.cover:
                    result = await self.storage_repo.delete_object(c.cover)
                if result:
                    await self.category_repo.delete_by_id(c.id)
                else:
                    status = False

            return OperationOutput(id=None, request="delete/categories-by-parent-id", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  