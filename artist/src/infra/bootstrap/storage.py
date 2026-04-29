from minio import Minio
from src.infra.schemas.storage.minio_client import MinioParams, MinioClient

def init_minio(
    params: MinioParams,    
) -> MinioParams:
    
    minio_client = Minio(
        params.host,
        access_key=params.access_key,
        secret_key=params.secret_key,
        secure=False,
    )
    
    return MinioClient(
        params=params,
        client=minio_client,
    )

async def init_storage_client(
    params: MinioParams,
) -> MinioClient:
    
    if isinstance(params, MinioParams):
        return init_minio(params)

async def terminate_storage_client(
    context: MinioClient | None = None,
):
    
    if not context:
        return
    
    if isinstance(context, MinioClient):
        pass