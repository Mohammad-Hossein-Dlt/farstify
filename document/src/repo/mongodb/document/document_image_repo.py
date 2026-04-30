from src.repo.interface.document.Idocument_image_repo import IDocumentImageRepo
from src.domain.schemas.document.document_image import DocumentImageModel
from src.infra.database.mongodb.collections.document.document_image_collection import DocumentImageCollection
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_object_id

class DocumentImageMongodbRepo(IDocumentImageRepo):
        
    async def create(
        self,
        image: DocumentImageModel,
    ) -> DocumentImageModel:
        
        new_document = await DocumentImageCollection(
            **image.model_dump(exclude={"id", "_id"}),
        ).insert()
        return DocumentImageModel.model_validate(new_document, from_attributes=True)
        
    async def get_by_id(
        self,
        image_id: str,
    ) -> DocumentImageModel:
        
        try:
                                    
            image_id = convert_object_id(image_id)
            
            image = await DocumentImageCollection.find_one(
                DocumentImageCollection.id == image_id,
            )
                        
            return DocumentImageModel.model_validate(image, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="document not found")

    async def update(
        self,
        image: DocumentImageModel,
    ) -> DocumentImageModel:
        
        try:               
            
            to_update: dict = image.custom_model_dump(
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await DocumentImageCollection.find(
                DocumentImageCollection.id == image.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                                    
            return await self.get_by_id(image.id)
        except EntityNotFoundError:
            raise
        
    async def delete_by_id(
        self,
        image_id: str,
    ) -> bool:
        
        try:
            image_id = convert_object_id(image_id)
            result = await DocumentImageCollection.find(
                DocumentImageCollection.id == image_id,
            ).delete()                       
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="document not found")
        
    async def get_by_document_id(
        self,
        document_id: str,
    ) -> list[DocumentImageModel]:
        
        try:
            document_id = convert_object_id(document_id)
            images_list = await DocumentImageCollection.find_many(
                DocumentImageCollection.document_id == document_id,
            ).to_list()            
            return [ DocumentImageModel.model_validate(image, from_attributes=True) for image in images_list ]
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="There are no documents")
    
    async def delete_by_document_id(
        self,
        document_id: str,
    ) -> bool:
        try:
            document_id = convert_object_id(document_id)
            result = await DocumentImageCollection.find(
                DocumentImageCollection.document_id == document_id
            ).delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="document not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            result = await DocumentImageCollection.find_all().delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="document not found")
