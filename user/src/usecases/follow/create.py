from src.repo.interface.follow.Ifollows_repo import IFollowsRepo, FollowModel
from src.models.schemas.follow.follow_input import FollowInput
from src.domain.schemas.follow.follow_model import FollowModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateFollow:
    
    def __init__(
        self,
        follow_repo: IFollowsRepo,
    ):
        
        self.follow_repo = follow_repo
    
    async def execute(
        self,
        entity: FollowInput,
    ) -> FollowModel | OperationOutput:
        
        try:
            follow_model: FollowModel = FollowModel.model_validate(entity, from_attributes=True)                
            try:
                check_unique: FollowModel = await self.follow_repo.check_unique(follow_model, entity.target_id)
                if check_unique:
                    status = await self.follow_repo.delete_by_id(check_unique.id, entity.target_id)
                    return OperationOutput(id=str(check_unique.id), request=f"unfollow/{entity.target_type}", status=status)
            except: ...
            return await self.follow_repo.create(follow_model, entity.target_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  