from src.repo.interface.user.Iuser_repo import IUserRepo
from src.models.schemas.user.create_user_input import CreateUserInput
from src.domain.schemas.user.user_model import UserModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateAllUsers:
    
    def __init__(
        self,
        user_repo: IUserRepo,
    ):
        
        self.user_repo = user_repo
    
    async def execute(
        self,
        users: list[CreateUserInput],
    ) -> UserModel:
        
        for user in users:
            
            try:
                user_model = UserModel.model_validate(user, from_attributes=True)
                await self.user_repo.create(user_model)
            except AppBaseException:
                raise
            except:
                raise OperationFailureException(500, "Internal server error")
            
        return OperationOutput(id=None, request="create/all_users", status=True)