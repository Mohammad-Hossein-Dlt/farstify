from src.repo.interface.like.Ilikes_repo import ILikesRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllLikes:
    
    def __init__(
        self,
        like_repo: ILikesRepo,
    ):
        
        self.like_repo = like_repo
    
    async def execute(
        self,
        user_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.like_repo.delete_by_user_id(user_id)
            return OperationOutput(id=user_id, request="unlike", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  