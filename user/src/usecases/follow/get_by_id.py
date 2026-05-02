from src.repo.interface.follow.Ifollow_repo import IFollowRepo
from src.domain.schemas.follow.follow_model import FollowModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetFollow:
    
    def __init__(
        self,
        follow_repo: IFollowRepo,
    ):
        
        self.follow_repo = follow_repo
    
    async def execute(
        self,
        target_id: str,
    ) -> FollowModel:
        
        try:
            return await self.follow_repo.get_by_id(target_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  