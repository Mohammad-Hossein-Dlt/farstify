from src.repo.interface.Iuser_repo import IUserRepo
from user.src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
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
            users: list[UserModel] = await self.user_repo.get_all(criteria)
            if isinstance(users, list):
                if criteria.order == "asc":
                    pass
                elif criteria.order == "desc":
                    users.reverse()
            return users
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  