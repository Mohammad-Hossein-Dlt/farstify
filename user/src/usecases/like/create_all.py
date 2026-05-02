from src.repo.interface.like.Ilikes_repo import ILikesRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

from test_data.like import likes
import random

class CreateAllLike:
    
    def __init__(
        self,
        like_repo: ILikesRepo,
    ):
        
        self.like_repo = like_repo
    
    async def execute(
        self,
    ) -> OperationOutput:
        
        try:
            await self.like_repo.delete_all()
            random.shuffle(likes)
            for i in likes:
                await self.like_repo.create(i)
            return OperationOutput(id=None, request="like-test", status=True)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  