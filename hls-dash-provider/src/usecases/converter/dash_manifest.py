from src.infra.schemas.converter.converter_params import ConverterParams
from src.repo.interface.Istorage_repo import IStorageRepo
from src.repo.interface.Icache import ICacheRepo
from src.gateway.interface.Ibroker_service import IBrokerService
from src.usecases.cache.get import GetCache
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.converter.dash_manifest import create_mpd_content
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
import tempfile
from pathlib import Path
import re

class CreateDashManifest:
    
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
            
            PTMS_list: list[str] = []
            reprs: list[str] = []
            
            for bitrate, manifest in cache.items():
                
                duration_match = re.search(r'mediaPresentationDuration="(?P<duration>[^"]+)"', manifest)
                duration = duration_match.groupdict().get("duration", None)
                if duration:
                    PTMS_list.append(duration)
                
                repr_match = re.findall(r'<Representation.*?</Representation>', manifest, re.DOTALL)
                if repr_match:
                    reprs.extend(repr_match)
                            
            with tempfile.TemporaryDirectory() as temp:
                
                temp_path = Path(temp)
                mpd_path = temp_path / "manifest.mpd"
                
                with open(mpd_path, "w", encoding="utf-8") as mpd_file:
                    content = create_mpd_content(PTMS_list, reprs)
                    mpd_file.write(content)
                
                result = await self.storage_repo.upload_object(
                    str(mpd_path),
                    str(object_path.parent).replace("\\", "/") + "/" + mpd_path.name,
                )
                
            if result:
                await self.storage_repo.delete_object(object_name)
            
            return OperationOutput(id=None, request="upload-object", status=result)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 