from src.repo.interface.Icategory_repo import ICategoryRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.category.update_category_input import UpdateCategoryInput
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.exceptions.exceptions import AppBaseException, EntityNotFoundError, InvalidRequestException, OperationFailureException
from pathlib import Path
import tempfile
import secrets

class UpdateCategory:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.category_repo = category_repo  
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        entity: UpdateCategoryInput,
        file: tempfile.SpooledTemporaryFile | None = None,
        file_name: str | None = None,
        file_size: int | None = None,
        content_type: str | None = None,
    ) -> CategoryModel:
        
        try:

            if entity.parent_id and entity.parent_id != entity.id:
                try:
                    parent: CategoryModel = await self.category_repo.get_by_id(entity.parent_id)
                    entity.parent_id = parent.id
                except EntityNotFoundError as ex:
                    raise EntityNotFoundError(ex.status_code, "Parent not found")
            elif entity.parent_id == entity.id:
                    raise InvalidRequestException(400, "Parent-id cannot be equal to id")
            
            category_model: CategoryModel = CategoryModel.model_validate(entity, from_attributes=True)
            category: CategoryModel = await self.category_repo.update(category_model)
            
            prev_cover = category.cover
            
            if all([file, file_name, file_size, content_type]):
                cover_name = secrets.token_hex(nbytes=5) + Path(file_name).suffix
                try:
                    result = await self.storage_repo.upload_object(
                        file,
                        cover_name,
                        file_size,
                        content_type,
                    )      
                    if result:
                        category.cover = cover_name 
                        category = await self.category_repo.update(category)
                        if category and prev_cover:
                            await self.storage_repo.delete_object(prev_cover)
                except:
                    category.cover = prev_cover
                    category = await self.category_repo.update(category)
                    await self.storage_repo.delete_object(cover_name)

            return category
            
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")