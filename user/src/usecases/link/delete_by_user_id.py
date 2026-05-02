from src.repo.interface.user.Iuser_link_repo import IUserLinkRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllLinks:
    
    def __init__(
        self,
        user_link_repo: IUserLinkRepo,
    ):
        
        self.user_link_repo = user_link_repo
    
    async def execute(
        self,
        user_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.user_link_repo.delete_by_user_id(user_id)
            return OperationOutput(id=user_id, request="delete/all-user-links", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  