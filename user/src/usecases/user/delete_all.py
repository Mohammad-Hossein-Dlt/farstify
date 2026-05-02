from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Iuser_image_repo import IUserImageRepo
from src.repo.interface.Iuser_link_repo import IUserLinkRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllUsers:
    
    def __init__(
        self,
        user_repo: IUserRepo,
        user_image_repo: IUserImageRepo,
        user_link_repo: IUserLinkRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.user_repo = user_repo
        self.user_image_repo = user_image_repo
        self.user_link_repo = user_link_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
    ) -> OperationOutput:
        
        try:
            status = await self.storage_repo.clean_dir()
            if status:
                await self.user_image_repo.delete_all()
                await self.user_link_repo.delete_all()
                status = await self.user_repo.delete_all()                    
            
            return OperationOutput(id=None, request="delete/all_users", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  