from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Iuser_image_repo import IUserImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.user.update_image_input import UpdateImageInput
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.user.user_image import UserImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
import tempfile
import secrets
from pathlib import Path

class UpdateImage:
    
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
        entity: UpdateImageInput,
        file: tempfile.SpooledTemporaryFile | None = None,
        file_name: str | None = None,
        file_size: int | None = None,
        content_type: str | None = None,
    ) -> UserImageModel:
        
        try:
            image_model: UserImageModel = UserImageModel.model_validate(entity, from_attributes=True)
            image: UserImageModel = await self.user_image_repo.get_by_id(entity.id)
            user: UserModel = await self.user_repo.get_by_id(image.user_id)
            prev_cover = image.cover
            if all([file, file_name, file_size, content_type]):
                cover_name = secrets.token_hex(nbytes=5) + Path(file_name).suffix
                base_path = f"{user.id}/image"
                new_object_name = f"{base_path}/{cover_name}"
                prev_object_name = f"{base_path}/{prev_cover}"
                try:
                    result = await self.storage_repo.upload_object(
                        file,
                        new_object_name,
                        file_size,
                        content_type,
                    )      
                    if result:
                        image_model.cover = cover_name
                        image: UserImageModel = await self.user_image_repo.update(image_model)
                        await self.storage_repo.delete_object(prev_object_name)
                except:
                    image.cover = prev_cover
                    image: UserImageModel = await self.user_image_repo.update(image)
                    await self.storage_repo.delete_object(new_object_name)
            else:
                image: UserImageModel = await self.user_image_repo.update(image_model)

            return image
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  