from src.repo.interface.like.Ilikes_repo import ILikesRepo, LikeModel
from src.models.schemas.like.like_input import LikeInput
from src.domain.schemas.like.like_model import LikeModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateLike:
    
    def __init__(
        self,
        like_repo: ILikesRepo,
    ):
        
        self.like_repo = like_repo
    
    async def execute(
        self,
        entity: LikeInput,
    ) -> LikeModel | OperationOutput:
        
        try:
            like_model: LikeModel = LikeModel.model_validate(entity, from_attributes=True)                
            try:
                check_unique: LikeModel = await self.like_repo.check_unique(like_model)
                if check_unique:
                    status = await self.like_repo.delete_by_id(check_unique.id)
                    return OperationOutput(id=str(check_unique.id), request=f"unlike", status=status)
            except: ...
            return await self.like_repo.create(like_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  