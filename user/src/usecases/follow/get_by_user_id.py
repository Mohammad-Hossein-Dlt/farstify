from src.repo.interface.follow.Ifollows_repo import IFollowsRepo
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.domain.schemas.follow.follow_model import FollowModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllFollows:
    
    def __init__(
        self,
        follow_repo: IFollowsRepo,
    ):
        
        self.follow_repo = follow_repo
    
    async def execute(
        self,
        user_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[FollowModel]:
        
        try:
            return await self.follow_repo.get_by_user_id(user_id, criteria)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  