from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.domain.schemas.episode.episode_model import EpisodeModel
from src.infra.database.mongodb.collections.episode.episode_collection import EpisodeCollection
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_object_id

class EpisodeMongodbRepo(IEpisodeRepo):
        
    async def create(
        self,
        episode: EpisodeModel,
    ) -> EpisodeModel:

        new_episode = await EpisodeCollection(
            **episode.model_dump(exclude={"id", "_id"}),
        ).insert()
        return EpisodeModel.model_validate(new_episode, from_attributes=True)
        
    async def get_by_id(
        self,
        episode_id: str,
    ) -> EpisodeModel:
        
        try:
                                    
            episode_id = convert_object_id(episode_id)
            
            episode = await EpisodeCollection.find_one(
                EpisodeCollection.id == episode_id,
            )
                        
            return EpisodeModel.model_validate(episode, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="episode not found")

    async def update(
        self,
        episode: EpisodeModel,
    ) -> EpisodeModel:
        
        try:               
            
            to_update: dict = episode.custom_model_dump(
                # exclude_unset=True,
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await EpisodeCollection.find(
                EpisodeCollection.id == episode.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get_by_id(episode.id)
        except EntityNotFoundError:
            raise
        
    async def delete_by_id(
        self,
        episode_id: str,
    ) -> bool:
        
        try:
            episode_id = convert_object_id(episode_id)
            delete_episode = await EpisodeCollection.find(
                EpisodeCollection.id == episode_id,
            ).delete()                       
            return bool(delete_episode.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="episode not found")
        
    async def get_by_document_id(
        self,
        document_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[EpisodeModel]:
        
        try:
            document_id = convert_object_id(document_id)
            episodes_list = await EpisodeCollection.find_many(
                EpisodeCollection.document_id == document_id,
            ).skip(
                criteria.page * criteria.limit
            ).limit(
                criteria.limit
            ).to_list()                  
            return [ EpisodeModel.model_validate(episode, from_attributes=True) for episode in episodes_list ]
        except:
            raise EntityNotFoundError(status_code=404, message="episode not found")
        
    async def delete_by_document_id(
        self,
        document_id: str,
    ) -> bool:
        
        try:
            document_id = convert_object_id(document_id)
            delete_episodes = await EpisodeCollection.find(
                EpisodeCollection.document_id == document_id,
            ).delete()                       
            return bool(delete_episodes.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="episode not found")
    
    async def get_all(
        self,
        criteria: BaseFilterCriteria,
    ) -> list[EpisodeModel]:    
        try:
            episodes_list = await EpisodeCollection.find_all().skip(
                criteria.page * criteria.limit
            ).limit(
                criteria.limit
            ).to_list()              
            return [ EpisodeModel.model_validate(episode, from_attributes=True) for episode in episodes_list ]
        except:
            raise EntityNotFoundError(status_code=404, message="episode not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            delete_episodes = await EpisodeCollection.delete_all()
            return bool(delete_episodes.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="episode not found")
