from src.repo.interface.user.Iuser_repo import IUserRepo
from src.repo.interface.user.Iuser_image_repo import IUserImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.user.create_image_input import CreateImageInput
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.user.user_image import UserImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
from pathlib import Path
import tempfile
import secrets

class CreateImage:
    
    def __init__(
        self,
        user_repo: IUserRepo,
        user_image_repo: IUserImageRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.user_repo = user_repo
        self.user_image_repo = user_image_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        entity: CreateImageInput,
        file: tempfile.SpooledTemporaryFile | None = None,
        file_name: str | None = None,
        file_size: int | None = None,
        content_type: str | None = None,
    ) -> UserImageModel:
        
        try:
            image_model: UserImageModel = UserImageModel.model_validate(entity, from_attributes=True)
            user: UserModel = await self.user_repo.get_by_id(entity.user_id)
            if all([file, file_name, file_size, content_type]):
                cover_name = secrets.token_hex(nbytes=5) + Path(file_name).suffix
                base_path = f"{user.id}/image"
                new_object_name = f"{base_path}/{cover_name}"
                try:
                    result = await self.storage_repo.upload_object(
                        file,
                        new_object_name,
                        file_size,
                        content_type,
                    )
                    if result:
                        image_model.cover = cover_name
                        image_model: UserImageModel = await self.user_image_repo.create(image_model)
                except:
                    if image_model.id:
                        await self.user_image_repo.delete_by_id(image_model.id)
                    await self.storage_repo.delete_object(new_object_name)

            return image_model
                        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  