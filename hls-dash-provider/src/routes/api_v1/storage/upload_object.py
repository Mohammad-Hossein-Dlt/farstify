from ._router import router
from fastapi import UploadFile, Depends, HTTPException
from src.domain.enums import Format
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.repo.interface.Icache import ICacheRepo
from src.routes.depends.cache_depend import cache_repo_depend
from src.gateway.interface.Ibroker_service import IBrokerService
from src.routes.depends.services_depend import convert_service_depend
from src.usecases.storage.upload_object import UploadObject
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/object/{object_name:path}",
)
async def upload_object(
    object_name: str,
    format: Format,
    file: UploadFile,
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
    cache_repo: ICacheRepo = Depends(cache_repo_depend),
    broker_service: IBrokerService = Depends(convert_service_depend),
):
    try:
        upload_file_usecase = UploadObject(storage_repo, cache_repo, broker_service)
        output = await upload_file_usecase.execute(
            object_name,
            format,
            file.file,
            file.filename,
            file.size,
            file.content_type,
        )
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))