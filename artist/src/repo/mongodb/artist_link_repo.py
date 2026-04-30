from src.repo.interface.Iartist_link_repo import IArtistLinkRepo
from src.domain.schemas.artist.artist_link import ArtistLinkModel
from src.infra.database.mongodb.collections.artist_link_collection import ArtistLinkCollection
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_object_id

class ArtistLinkMongodbRepo(IArtistLinkRepo):
        
    async def create(
        self,
        link: ArtistLinkModel,
    ) -> ArtistLinkModel:
        
        new_link = await ArtistLinkCollection(
            **link.model_dump(exclude={"id", "_id"}),
        ).insert()
        return ArtistLinkModel.model_validate(new_link, from_attributes=True)
        
    async def get_by_id(
        self,
        link_id: str,
    ) ->  ArtistLinkModel:
        
        try:
                                    
            link_id = convert_object_id(link_id)
            
            link = await ArtistLinkCollection.find_one(
                ArtistLinkCollection.id == link_id,
            )
                        
            return ArtistLinkModel.model_validate(link, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Artist not found")

    async def update(
        self,
        link: ArtistLinkModel,
    ) ->  ArtistLinkModel:
        
        try:               
            
            to_update: dict = link.custom_model_dump(
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await ArtistLinkCollection.find(
                ArtistLinkCollection.id == link.id,
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
            result = await ArtistLinkCollection.find(
                ArtistLinkCollection.id == link_id,
            ).delete()                       
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Artist not found")
        
    async def get_by_artist_id(
        self,
        artist_id: str,
    ) ->  list[ArtistLinkModel]:
        
        try:
            artist_id = convert_object_id(artist_id)
            links_list = await ArtistLinkCollection.find_many(
                ArtistLinkCollection.artist_id == artist_id,
            ).to_list()
            return [ ArtistLinkModel.model_validate(link, from_attributes=True) for link in links_list ]
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="There are no artists")
    
    async def delete_by_artist_id(
        self,
        artist_id: str,
    ) -> bool:
        try:
            artist_id = convert_object_id(artist_id)
            result = await ArtistLinkCollection.find(
                ArtistLinkCollection.artist_id == artist_id
            ).delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="Artist not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            result = await ArtistLinkCollection.find_all().delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="Artist not found")
