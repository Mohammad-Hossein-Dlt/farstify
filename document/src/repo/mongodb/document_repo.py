from src.repo.interface.Idocument_repo import IDocumentRepo
from src.domain.schemas.document.document_model import DocumentModel
from src.infra.database.mongodb.collections.document_collection import DocumentCollection
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_object_id

class DocumentMongodbRepo(IDocumentRepo):
        
    async def create(
        self,
        document: DocumentModel,
    ) -> DocumentModel:

        new_document = await DocumentCollection(
            **document.model_dump(exclude={"id", "_id"}),
        ).insert()
        return DocumentModel.model_validate(new_document, from_attributes=True)
        
    async def get_by_id(
        self,
        document_id: str,
    ) ->  DocumentModel:
        
        try:
                                    
            document_id = convert_object_id(document_id)
            
            document = await DocumentCollection.find_one(
                DocumentCollection.id == document_id,
            )
                        
            return DocumentModel.model_validate(document, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="document not found")

    async def update(
        self,
        document: DocumentModel,
    ) ->  DocumentModel:
        
        try:               
            
            to_update: dict = document.custom_model_dump(
                # exclude_unset=True,
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await DocumentCollection.find(
                DocumentCollection.id == document.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get_by_id(document.id)
        except EntityNotFoundError:
            raise
        
    async def delete_by_id(
        self,
        document_id: str,
    ) -> bool:
        
        try:
            document_id = convert_object_id(document_id)
            delete_document = await DocumentCollection.find(
                DocumentCollection.id == document_id,
            ).delete()                       
            return bool(delete_document.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="document not found")
    
    async def get_all(
        self,
    ) -> list[DocumentModel]:    
        try:
            documents_list = await DocumentCollection.find_all().to_list()            
            return [ DocumentModel.model_validate(document, from_attributes=True) for document in documents_list ]
        except:
            raise EntityNotFoundError(status_code=404, message="document not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            delete_documents = await DocumentCollection.delete_all()
            return bool(delete_documents.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="document not found")
