from src.repo.interface.user.Iuser_repo import IUserRepo
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllUsers:
    
    def __init__(
        self,
        user_repo: IUserRepo,
    ):
        
        self.user_repo = user_repo  
    
    async def execute(
        self,
        criteria: BaseFilterCriteria,
    ) -> list[UserModel]:
        
        try:
            return await self.user_repo.get_all(criteria)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  