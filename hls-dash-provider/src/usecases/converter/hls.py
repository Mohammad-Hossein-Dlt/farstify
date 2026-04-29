from src.infra.schemas.converter.converter_params import ConverterParams
from src.repo.interface.Istorage_repo import IStorageRepo
from src.repo.interface.Icache import ICacheRepo
from src.gateway.interface.Ibroker_service import IBrokerService
from src.usecases.cache.save import SaveCache
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.converter.hls import hls_command
from src.domain.enums import Format
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
from urllib3 import BaseHTTPResponse
import tempfile
from pathlib import Path
import subprocess

class HlsConverter:
    
    def __init__(
        self,
        converter_params: ConverterParams,
        storage_repo: IStorageRepo,
        cache_repo: ICacheRepo,
        broker_service: IBrokerService,
    ):
        
        self.converter_params = converter_params
        self.storage_repo = storage_repo
        self.save_cache_usecase = SaveCache(cache_repo)
        self.broker_service = broker_service
    
    async def execute(
        self,
        object_name: str,
    ) -> OperationOutput:
        
        try:
            
            object_path = Path(object_name)
            response: BaseHTTPResponse = await self.storage_repo.get_object(object_name)

            with tempfile.TemporaryDirectory() as temp:
                                                                
                command, ts_path, m3u8_path = hls_command(temp, "pipe:0", self.converter_params.bitrate)
                      
                process = subprocess.Popen(
                    command,
                    stdin=subprocess.PIPE,
                )
                
                for chunk in response.stream( 64 * 1024 ):
                    # RAM usage 64 kb
                    if process.poll() is not None:
                        break
                    process.stdin.write(chunk)
                    
                process.stdin.close()
                process.wait()
                
                result = await self.storage_repo.upload_objects(
                    temp,
                    f"{object_path.parent}/",
                )
                
                data = await self.save_cache_usecase.execute(
                    f"convert:{object_path}",
                    {
                        self.converter_params.bitrate: True
                    },
                )
                
                if self.converter_params.number == len(data):
                    await self.broker_service.create_stream_file(object_name, Format.hls)
            
            return OperationOutput(id=None, request="upload-object", status=result)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 