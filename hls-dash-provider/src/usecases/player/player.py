from src.repo.interface.Istorage_repo import IStorageRepo
from src.domain.enums import Format
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class Player:
    
    def __init__(
        self,
        storage_repo: IStorageRepo,
    ):
        
        self.storage_repo = storage_repo
    
    def execute(
        self,
        object_name: str,
        format: Format,
    ) -> str:
        
        try:
            
            url = f"http://localhost:9001/{object_name}"
            
            if not url.endswith("/"):
                url += "/"
                
            if format == "dash":
                url += "manifest.mpd"
            elif format == "hls":
                url += "master.m3u8"
                            
            return url
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 