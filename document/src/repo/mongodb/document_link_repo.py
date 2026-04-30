from src.repo.interface.Idocument_link_repo import IDocumentLinkRepo
from src.domain.schemas.document.document_link import DocumentLinkModel
from src.infra.database.mongodb.collections.document_link_collection import DocumentLinkCollection
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_object_id

class DocumentLinkMongodbRepo(IDocumentLinkRepo):
        
    async def create(
        self,
        link: DocumentLinkModel,
    ) -> DocumentLinkModel:
        
        new_link = await DocumentLinkCollection(
            **link.model_dump(exclude={"id", "_id"}),
        ).insert()
        return DocumentLinkModel.model_validate(new_link, from_attributes=True)
        
    async def get_by_id(
        self,
        link_id: str,
    ) ->  DocumentLinkModel:
        
        try:
                                    
            link_id = convert_object_id(link_id)
            
            link = await DocumentLinkCollection.find_one(
                DocumentLinkCollection.id == link_id,
            )
                        
            return DocumentLinkModel.model_validate(link, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="document not found")

    async def update(
        self,
        link: DocumentLinkModel,
    ) ->  DocumentLinkModel:
        
        try:               
            
            to_update: dict = link.custom_model_dump(
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await DocumentLinkCollection.find(
                DocumentLinkCollection.id == link.id,
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
            result = await DocumentLinkCollection.find(
                DocumentLinkCollection.id == link_id,
            ).delete()                       
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="document not found")
        
    async def get_by_document_id(
        self,
        document_id: str,
    ) ->  list[DocumentLinkModel]:
        
        try:
            document_id = convert_object_id(document_id)
            links_list = await DocumentLinkCollection.find_many(
                DocumentLinkCollection.document_id == document_id,
            ).to_list()
            return [ DocumentLinkModel.model_validate(link, from_attributes=True) for link in links_list ]
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="There are no documents")
    
    async def delete_by_document_id(
        self,
        document_id: str,
    ) -> bool:
        try:
            document_id = convert_object_id(document_id)
            result = await DocumentLinkCollection.find(
                DocumentLinkCollection.document_id == document_id
            ).delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="document not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            result = await DocumentLinkCollection.find_all().delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="document not found")
