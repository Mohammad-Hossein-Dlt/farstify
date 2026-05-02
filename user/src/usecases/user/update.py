from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.user.update_user_input import UpdateUserInput
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateUser:
    
    def __init__(
        self,
        user_repo: IUserRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.user_repo = user_repo  
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        entity: UpdateUserInput,
    ) -> UserModel:
        
        try:
            user_model: UserModel = UserModel.model_validate(entity, from_attributes=True)
            return await self.user_repo.update(user_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")