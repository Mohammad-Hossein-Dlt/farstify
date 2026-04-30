from src.repo.interface.episode.Iepisode_link_repo import IEpisodeLinkRepo
from src.domain.schemas.episode.episode_link import EpisodeLinkModel
from src.infra.database.mongodb.collections.episode.episode_link_collection import EpisodeLinkCollection
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_object_id

class EpisodeLinkMongodbRepo(IEpisodeLinkRepo):
        
    async def create(
        self,
        link: EpisodeLinkModel,
    ) -> EpisodeLinkModel:
        
        new_link = await EpisodeLinkCollection(
            **link.model_dump(exclude={"id", "_id"}),
        ).insert()
        return EpisodeLinkModel.model_validate(new_link, from_attributes=True)
        
    async def get_by_id(
        self,
        link_id: str,
    ) ->  EpisodeLinkModel:
        
        try:
                                    
            link_id = convert_object_id(link_id)
            
            link = await EpisodeLinkCollection.find_one(
                EpisodeLinkCollection.id == link_id,
            )
                        
            return EpisodeLinkModel.model_validate(link, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="episode not found")

    async def update(
        self,
        link: EpisodeLinkModel,
    ) ->  EpisodeLinkModel:
        
        try:               
            
            to_update: dict = link.custom_model_dump(
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await EpisodeLinkCollection.find(
                EpisodeLinkCollection.id == link.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get_by_id(link.id)
        except EntityNotFoundError:
            raise
        
    async def delete_by_id(
        self,
        link_id: str,
    ) -> bool:
        
        try:
            link_id = convert_object_id(link_id)
            result = await EpisodeLinkCollection.find(
                EpisodeLinkCollection.id == link_id,
            ).delete()                       
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="episode not found")
        
    async def get_by_episode_id(
        self,
        episode_id: str,
    ) ->  list[EpisodeLinkModel]:
        
        try:
            episode_id = convert_object_id(episode_id)
            links_list = await EpisodeLinkCollection.find_many(
                EpisodeLinkCollection.episode_id == episode_id,
            ).to_list()
            return [ EpisodeLinkModel.model_validate(link, from_attributes=True) for link in links_list ]
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="There are no episodes")
    
    async def delete_by_episode_id(
        self,
        episode_id: str,
    ) -> bool:
        try:
            episode_id = convert_object_id(episode_id)
            result = await EpisodeLinkCollection.find(
                EpisodeLinkCollection.episode_id == episode_id
            ).delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="episode not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            result = await EpisodeLinkCollection.find_all().delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="episode not found")
