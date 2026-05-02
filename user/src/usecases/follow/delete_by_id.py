from src.repo.interface.follow.Ifollows_repo import IFollowsRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteFollow:
    
    def __init__(
        self,
        follow_repo: IFollowsRepo,
    ):
        
        self.follow_repo = follow_repo
    
    async def execute(
        self,
        target_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.follow_repo.delete_by_id(target_id)
            return OperationOutput(id=target_id, request="unfollow", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  