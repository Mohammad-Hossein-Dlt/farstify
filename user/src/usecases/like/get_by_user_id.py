from src.repo.interface.like.Ilikes_repo import ILikesRepo
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.domain.schemas.like.like_model import LikeModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllLikes:
    
    def __init__(
        self,
        like_repo: ILikesRepo,
    ):
        
        self.like_repo = like_repo
    
    async def execute(
        self,
        user_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[LikeModel]:
        
        try:
            return await self.like_repo.get_by_user_id(user_id, criteria)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  