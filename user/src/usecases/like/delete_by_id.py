from src.repo.interface.like.Ilikes_repo import ILikesRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteLike:
    
    def __init__(
        self,
        like_repo: ILikesRepo,
    ):
        
        self.like_repo = like_repo
    
    async def execute(
        self,
        target_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.like_repo.delete_by_id(target_id)
            return OperationOutput(id=target_id, request="unlike", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  