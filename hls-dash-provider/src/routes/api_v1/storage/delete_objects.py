from ._router import router
from fastapi import Depends, HTTPException
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.storage.delete_objects import DeleteObjects
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/objects",
)
async def delete_objects(
    path: str,
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        upload_file_usecase = DeleteObjects(storage_repo)
        output = await upload_file_usecase.execute(path)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))