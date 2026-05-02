from src.repo.interface.like.Ilikes_repo import ILikesRepo
from src.domain.schemas.like.like_model import LikeModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetLike:
    
    def __init__(
        self,
        like_repo: ILikesRepo,
    ):
        
        self.like_repo = like_repo
    
    async def execute(
        self,
        target_id: str,
    ) -> LikeModel:
        
        try:
            return await self.like_repo.get_by_id(target_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  