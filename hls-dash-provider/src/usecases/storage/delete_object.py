from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteObject:
    
    def __init__(
        self,
        storage_repo: IStorageRepo,
    ):
        
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        storage_path: str,
    ) -> OperationOutput:
        
        try:
            status = False
            check_object = await self.storage_repo.get_object_stat(storage_path)
            if check_object:
                status = await self.storage_repo.delete_object(storage_path)
            return OperationOutput(id=None, request="delete-object", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 