from src.repo.interface.follow.Ifollow_repo import IFollowRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

from test_data.follow import artist, document, episode

class CreateAllFollow:
    
    def __init__(
        self,
        follow_repo: IFollowRepo,
    ):
        
        self.follow_repo = follow_repo
    
    async def execute(
        self,
    ) -> OperationOutput:
        
        try:
            await self.follow_repo.delete_all()
            for i in artist:
                await self.follow_repo.create(i)
            for i in document:
                await self.follow_repo.create(i)
            for i in episode:
                await self.follow_repo.create(i)
            return OperationOutput(id=None, request="follow-test", status=True)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  