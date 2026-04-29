from src.repo.interface.Istorage_repo import IStorageRepo
from src.repo.interface.Icache import ICacheRepo
from src.gateway.interface.Ibroker_service import IBrokerService
from src.usecases.cache.delete import DeleteCache
from src.domain.enums import Format
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
import tempfile

class UploadObject:
    
    def __init__(
        self,
        storage_repo: IStorageRepo,
        cache_repo: ICacheRepo,
        broker_service: IBrokerService,
    ):
        
        self.storage_repo = storage_repo
        self.delete_cache_usecase = DeleteCache(cache_repo)
        self.broker_service = broker_service
    
    async def execute(
        self,
        path: str,
        format: Format,
        file: tempfile.SpooledTemporaryFile | str,
        file_name: str,
        file_size: int | None = None,
        content_type: str | None = None,
    ) -> OperationOutput:
        
        try:
            
            
            object_name = path
            if path.endswith("/"):
                object_name += file_name
            else:
                object_name += "/" + file_name
            
            await self.delete_cache_usecase.execute(f"convert:{object_name}")
                        
            result = await self.storage_repo.upload_object(
                file,
                object_name,
                file_size,
                content_type,
            )
            
            if result:
                await self.broker_service.convert(object_name, format)
            
            return OperationOutput(id=None, request="upload-object", status=result)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 