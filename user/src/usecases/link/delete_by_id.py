from src.repo.interface.Iuser_link_repo import IUserLinkRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteLink:
    
    def __init__(
        self,
        user_link_repo: IUserLinkRepo,
    ):
        
        self.user_link_repo = user_link_repo
    
    async def execute(
        self,
        link_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.user_link_repo.delete_by_id(link_id)
            return OperationOutput(id=link_id, request="delete/user-link", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  