from src.repo.interface.follow.Ifollow_repo import IFollowRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllFollows:
    
    def __init__(
        self,
        follow_repo: IFollowRepo,
    ):
        
        self.follow_repo = follow_repo
    
    async def execute(
        self,
        user_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.follow_repo.delete_by_user_id(user_id)
            return OperationOutput(id=user_id, request="unfollow", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  