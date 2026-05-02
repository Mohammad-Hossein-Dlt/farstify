from src.repo.interface.follow.Ifollow_repo import IFollowRepo, FollowModel
from src.models.schemas.user.create_follow_input import CreateFollowInput
from src.domain.schemas.follow.follow_model import FollowModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateFollow:
    
    def __init__(
        self,
        follow_repo: IFollowRepo,
    ):
        
        self.follow_repo = follow_repo
    
    async def execute(
        self,
        entity: CreateFollowInput,
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