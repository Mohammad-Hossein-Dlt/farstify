from src.repo.interface.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetUser:
    
    def __init__(
        self,
        user_repo: IUserRepo,
    ):
        
        self.user_repo = user_repo  
    
    async def execute(
        self,
        user_id: str,
    ) -> UserModel:
        
        try:
            return await self.user_repo.get_by_id(user_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")