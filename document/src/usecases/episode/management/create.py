from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.episode.create_episode_input import CreateEpisodeInput
from src.domain.schemas.episode.episode_model import EpisodeModel
from src.domain.schemas.document.document_model import DocumentModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
import tempfile
from pathlib import Path

class CreateEpisode:
    
    def __init__(
        self,
        episode_repo: IEpisodeRepo,
        document_repo: IDocumentRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.episode_repo = episode_repo
        self.document_repo = document_repo
        self.storage_repo = storage_repo
    
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
                try:
                    cover_name = "file" + Path(file_name).suffix
                    result = await self.storage_repo.upload_object(
                        file,
                        f"{document.id}/{episode.id}/{cover_name}",
                        file_size,
                        content_type,
                    )
                    if not result:
                        await self.storage_repo.delete_object(f"{document.id}/{episode.id}/{cover_name}")
                except:
                    await self.storage_repo.delete_object(f"{document.id}/{episode.id}/{cover_name}")
                    
            return episode
        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  