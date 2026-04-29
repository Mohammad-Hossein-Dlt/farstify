from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteObjects:
    
    def __init__(
        self,
        storage_repo: IStorageRepo,
    ):
        
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        path: str,
    ) -> OperationOutput:
        
        try:
            check_path = await self.storage_repo.path_objects(path)
            status = False
            if check_path:
                status = await self.storage_repo.delete_objects(path)
            return OperationOutput(id=None, request="delete-objects", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 