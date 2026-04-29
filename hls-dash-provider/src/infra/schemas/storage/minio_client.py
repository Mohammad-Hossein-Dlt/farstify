from minio import Minio
from .storage_params import BaseStorageParams
from .storage_client import BaseStorageClient
from pydantic import BaseModel, ConfigDict

class MinioParams(BaseStorageParams):
    host: str
    access_key: str
    secret_key: str
    
class MinioClient(BaseStorageClient, BaseModel):
    params: MinioParams
    client: Minio

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    def get_dependency(self):
        yield self.client
