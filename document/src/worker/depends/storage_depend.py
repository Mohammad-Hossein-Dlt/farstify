from faststream import Depends
from src.infra.context.app_context import AppContext
from src.repo.interface.Istorage_repo import IStorageRepo
from src.repo.storage.minio_repo import MinioRepo
from minio import Minio

def storage_client_depend():    
    client = AppContext.storage_client
    yield from client.get_dependency()

def storage_repo_depend(
    client: Minio = Depends(storage_client_depend),
) -> IStorageRepo:
    
    if isinstance(client, Minio):        
        return MinioRepo(client, "document")