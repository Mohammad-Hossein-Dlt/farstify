from src.repo.interface.Icategory_repo import ICategoryRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllCategories:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
        storage_repo: IStorageRepo,
    ):        
        
        self.category_repo = category_repo   
        self.storage_repo = storage_repo
    
    async def execute(
        self,
    ) -> OperationOutput:
        
        try:
            await self.storage_repo.clean_dir()
            status = await self.category_repo.delete_all()                    
            return OperationOutput(id=None, request="delete/all-categories", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  