from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Iuser_image_repo import IUserImageRepo
from src.repo.interface.Iuser_link_repo import IUserLinkRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteUser:
    
    def __init__(
        self,
        user_repo: IUserRepo,
        user_image_repo: IUserImageRepo,
        user_link_repo: IUserLinkRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.user_repo = user_repo
        self.user_image_repo = user_image_repo
        self.user_link_repo = user_link_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        user_id: str,
    ) -> OperationOutput:
        
        try:
            status = False
            user: UserModel = await self.user_repo.get_by_id(user_id)
            check_path = await self.storage_repo.path_objects(str(user.id))
            if check_path:
                delete_objects = await self.storage_repo.delete_objects(str(user.id))
                if delete_objects:
                    await self.user_image_repo.delete_by_user_id(user_id)
                    await self.user_link_repo.delete_by_user_id(user_id)
                    status = await self.user_repo.delete_by_id(user_id)
            else:
                await self.user_image_repo.delete_by_user_id(user_id)
                await self.user_link_repo.delete_by_user_id(user_id)
                status = await self.user_repo.delete_by_id(user_id)
            
            return OperationOutput(id=user_id, request="delete/user", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  