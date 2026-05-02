from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Iuser_image_repo import IUserImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.user.user_image import UserImageModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllImages:
    
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
        user_id: str,
    ) -> OperationOutput:
        
        try:
            user: UserModel = await self.user_repo.get_by_id(user_id)
            images: list[UserImageModel] = await self.user_image_repo.get_by_user_id(user_id)
            
            status = True if images else False
            for i in images:
                result = await self.storage_repo.delete_object(f"{user.id}/" + "image/" + i.cover)
                if result:
                    await self.user_image_repo.delete_by_id(i.id)
                else:
                    status = False
            
            return OperationOutput(id=user_id, request="delete/all-user-images", status=status)        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  