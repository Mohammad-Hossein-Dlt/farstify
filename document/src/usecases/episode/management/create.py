from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.gateway.interface.Ibroker_service import IBrokerService
from src.models.schemas.episode.create_episode_input import CreateEpisodeInput
from src.domain.schemas.episode.episode_model import EpisodeModel
from src.domain.schemas.document.document_model import DocumentModel
from src.domain.enums import Format
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
import tempfile
from pathlib import Path

class CreateEpisode:
    
    def __init__(
        self,
        document_repo: IDocumentRepo,
        episode_repo: IEpisodeRepo,
        cache_repo: ICacheRepo,
        storage_repo: IStorageRepo,
        broker_service: IBrokerService,
    ):
        
        self.document_repo = document_repo
        self.episode_repo = episode_repo
        self.cache_repo = cache_repo
        self.storage_repo = storage_repo
        self.broker_service = broker_service
    
    async def execute(
        self,
        entity: CreateEpisodeInput,
        file: tempfile.SpooledTemporaryFile | None = None,
        file_name: str | None = None,
        file_size: int | None = None,
        content_type: str | None = None,
    ) -> EpisodeModel:
        
        try:
            episode_model: EpisodeModel = EpisodeModel.model_validate(entity, from_attributes=True)
            document: DocumentModel = await self.document_repo.get_by_id(entity.document_id)
            episode: EpisodeModel = await self.episode_repo.create(episode_model)
            if all([file, file_name, file_size, content_type]):
                cover_name = "file" + Path(file_name).suffix
                base_path = f"{document.id}/{episode.id}/audio"
                new_object_name = f"{base_path}/{cover_name}"
                delete_prev = await self.storage_repo.delete_objects(base_path)
                if delete_prev:
                    try:
                        result = await self.storage_repo.upload_object(
                            file,
                            new_object_name,
                            file_size,
                            content_type,
                        )
                        if result:
                            self.cache_repo.delete(f"convert:{new_object_name}")
                            await self.broker_service.convert(new_object_name, Format.dash)
                        else:
                            await self.storage_repo.delete_object(new_object_name)
                    except:
                        await self.storage_repo.delete_object(new_object_name)
                    
            return episode
        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  