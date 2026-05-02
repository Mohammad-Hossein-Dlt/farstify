from src.repo.interface.user.Iuser_repo import IUserRepo
from src.repo.interface.user.Iuser_image_repo import IUserImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.domain.schemas.user.user_image import UserImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetImage:
    
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
    ) -> UserImageModel:
        
        try:
            return await self.user_image_repo.get_by_id(image_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  