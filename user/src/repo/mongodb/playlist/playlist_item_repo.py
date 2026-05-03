from src.repo.interface.playlist.Iplaylist_item_repo import IPlaylistItemRepo
from src.domain.schemas.playlist.playlist_item_model import PlaylistItemModel
from src.infra.database.mongodb.collections.playlist.playlist_item_collection import PlaylistItemCollection
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_object_id

class PlaylistItemMongodbRepo(IPlaylistItemRepo):
                
    async def create(
        self,
        item: PlaylistItemModel,
    ) -> PlaylistItemModel:
        
        try:
            new_user = await PlaylistItemCollection(
                **item.model_dump(exclude={"id", "_id"}),
            ).insert()
            return PlaylistItemModel.model_validate(new_user, from_attributes=True)
        except:
            ...

    async def get_by_id(
        self,
        item_id: str,
    ) -> PlaylistItemModel:
        
        try:
            item_id = convert_object_id(item_id)
            playlist = await PlaylistItemCollection.find_one(
                PlaylistItemCollection.id == item_id,
            )
                        
            return PlaylistItemModel.model_validate(playlist, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Playlist not found")

    async def update(
        self,
        playlist: PlaylistItemModel,
    ) -> PlaylistItemModel:
        
        try:               
            to_update: dict = playlist.custom_model_dump(
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await PlaylistItemCollection.find(
                PlaylistItemCollection.id == playlist.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                                    
            return await self.get_by_id(playlist.id)
        except EntityNotFoundError:
            raise
        
    async def delete_by_id(
        self,
        item_id: str,
    ) -> bool:
        
        try:
            item_id = convert_object_id(item_id)
            result = await PlaylistItemCollection.find(
                PlaylistItemCollection.id == item_id,
            ).delete()                       
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Playlist not found")
        
    async def get_by_playlist_id(
        self,
        playlist_id: str,
        criteria: BaseFilterCriteria | None = None,
    ) -> list[PlaylistItemModel]:
        
        try:
            playlist_id = convert_object_id(playlist_id)
            query = PlaylistItemCollection.find_many(
                PlaylistItemCollection.playlist_id == playlist_id,
            )
            
            if criteria:
                query.skip(
                    criteria.page * criteria.limit
                ).limit(
                    criteria.limit
                ).sort(
                    PlaylistItemCollection.created_at if criteria.order == "asc" else -PlaylistItemCollection.created_at
                )
            
            items_list = await query.to_list()
            return [ PlaylistItemModel.model_validate(playlist, from_attributes=True) for playlist in items_list ]
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="There are no playlists")
    
    async def delete_by_playlist_id(
        self,
        playlist_id: str,
    ) -> bool:
        try:
            playlist_id = convert_object_id(playlist_id)
            result = await PlaylistItemCollection.find(
                PlaylistItemCollection.playlist_id == playlist_id
            ).delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="Playlist not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            result = await PlaylistItemCollection.find_all().delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="Playlist not found")
