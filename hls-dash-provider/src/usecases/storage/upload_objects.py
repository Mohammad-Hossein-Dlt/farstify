from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
import secrets

class UploadObjects:
    
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
            result = await self.storage_repo.upload_objects(
                path,
                secrets.token_hex()[0:16] + "/",
            )
            
            return OperationOutput(id=None, request="upload-objects", status=result)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 