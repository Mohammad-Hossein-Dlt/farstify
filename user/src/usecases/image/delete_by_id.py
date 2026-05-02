from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Iuser_image_repo import IUserImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.user.user_image import UserImageModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteImage:
    
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
        image_id: str,
    ) -> OperationOutput:
        
        try:
            
            image: UserImageModel = await self.user_image_repo.get_by_id(image_id)
            user: UserModel = await self.user_repo.get_by_id(image.user_id)
            
            result = await self.storage_repo.delete_object(f"{user.id}/" + "image/" + image.cover)
            
            status = False
            if result:
                status = await self.user_image_repo.delete_by_id(image.id)

            return OperationOutput(id=image_id, request="delete/user-image", status=status)
        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  