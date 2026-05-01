from src.infra.schemas.converter.converter_params import ConverterParams
from src.repo.interface.Istorage_repo import IStorageRepo
from src.repo.interface.Icache import ICacheRepo
from src.gateway.interface.Ibroker_service import IBrokerService
from src.usecases.cache.get import GetCache
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.converter.hls_master import create_m3u8_content
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
import tempfile
from pathlib import Path

class CreateHlsMaster:
    
    def __init__(
        self,
        converter_params: ConverterParams,
        storage_repo: IStorageRepo,
        cache_repo: ICacheRepo,
        broker_service: IBrokerService,
    ):
        
        self.converter_params = converter_params
        self.storage_repo = storage_repo
        self.get_cache_usecase = GetCache(cache_repo)
        self.broker_service = broker_service
    
    async def execute(
        self,
        object_name: str,
    ) -> OperationOutput:
        
        try:
            
            object_path = Path(object_name)
            cache = await self.get_cache_usecase.execute(f"convert:{object_path}")
            
            if not isinstance(cache, dict):
                raise ValueError()
            
            cache = dict(sorted(cache.items(), key=lambda x: x[0]))
            
            bitrates: list[int] = []

            for bitrate, status in cache.items():
                if status:
                    bitrates.append(int(bitrate))
                    
            with tempfile.TemporaryDirectory() as temp:
                
                temp_path = Path(temp)
                m3u8_path = temp_path / "master.m3u8"
                
                with open(m3u8_path, "w", encoding="utf-8") as mpd_file:
                    content = create_m3u8_content(bitrates)
                    mpd_file.write(content)
                
                result = await self.storage_repo.upload_object(
                    str(m3u8_path),
                    str(object_path.parent).replace("\\", "/") + "/" + m3u8_path.name,
                )

            if result:
                await self.storage_repo.delete_object(object_name)
                
            return OperationOutput(id=None, request="upload-object", status=result)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 