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
        object_name: str,
    ) -> OperationOutput:
        
        try:
            check_object = await self.storage_repo.get_object_stat(object_name)
            status = False
            if check_object:
                status = await self.storage_repo.delete_object(object_name)
            return OperationOutput(id=None, request="delete-object", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 