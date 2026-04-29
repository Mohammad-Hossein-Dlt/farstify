from src.repo.interface.Icategory_repo import ICategoryRepo
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.database.mongodb.collections.category_collection import CategoryCollection
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
from src.infra.exceptions.exceptions import EntityNotFoundError, DuplicateEntityError
from src.infra.utils.convert_id import convert_object_id

from beanie.operators import And, Or, NotIn

class CategoryMongodbRepo(ICategoryRepo):
        
    async def create_category(
        self,
        category: CategoryModel,
    ) -> CategoryModel:
        
        try:
            await self.check_category(category)
            raise DuplicateEntityError(409, "Category already exist")
        except EntityNotFoundError:
            new_category = await CategoryCollection.insert(
                CategoryCollection(**category.model_dump(exclude={"id", "_id"})),
            )
            return CategoryModel.model_validate(new_category, from_attributes=True)
    
    async def check_category(
        self,
        category: CategoryModel,
    ) -> CategoryModel:
        
        try:
            result = await CategoryCollection.find_one(
                And(
                    CategoryCollection.slug == category.slug,                    
                    CategoryCollection.name == category.name,                    
                ),
            )
            return CategoryModel.model_validate(result, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Category not found")
        
    async def get_category_by_id(
        self,
        category_id: str,
    ) ->  CategoryModel:
        
        try:
                                    
            category_id = convert_object_id(category_id)
            
            category = await CategoryCollection.find_one(
                CategoryCollection.id == category_id,
            )
                        
            return CategoryModel.model_validate(category, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Category not found")
        
    async def update_category(
        self,
        category: CategoryModel,
    ) ->  CategoryModel:
        
        try:               
            
            to_update: dict = category.custom_model_dump(
                exclude_unset=True,
                exclude_none=True,
                exclude={
                    "id",
                },
                db_stack="no-sql",
            )
            
            await CategoryCollection.find(
                CategoryCollection.id == category.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get_category_by_id(category.id)
        except EntityNotFoundError:
            raise
        
    async def delete_category(
        self,
        category_id: str,
    ) -> bool:
        
        try:
            category_id = convert_object_id(category_id)
            result = await CategoryCollection.find(
                CategoryCollection.id == category_id,
            ).delete()                       
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Category not found")
        
    async def get_all_categories(
        self,
    ) -> list[CategoryModel]:
        
        try:
            categories_list = await CategoryCollection.find_all().to_list()
            return [ CategoryModel.model_validate(category, from_attributes=True) for category in categories_list ]
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="Categories not found")
        
    async def get_categories_with_filter(
        self,
        filter: CategoryFilterInput,
    ) -> list[CategoryModel]:
        
        try:
            if filter.based_on == "parent-id":
                return await self.get_parent_to_child(filter)
            elif filter.based_on == "child-to-parent":
                return await self.get_child_to_parent(filter)
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="Categories not found")
    
    async def get_parent_to_child(
        self,
        filter: CategoryFilterInput,
    ) -> list[CategoryModel]:
        
        parents_list = await self.get_categories_by_parent_id(filter.id, filter.contains_danglings)
            
        for parent in parents_list:
            children = await self.get_categories_by_parent_id(parent.id, filter.contains_danglings)
            
            if children:
                setattr(parent, "children", children)
                
        return parents_list
    
    async def get_child_to_parent(
        self,
        filter: CategoryFilterInput,
    ) ->  list[CategoryModel]:
        
        async def get_categories(
            p_id: str | None = None,
        ) -> list[CategoryModel]:
                     
            result: list[CategoryModel] = []
            if not p_id:
                return result
                          
            category = await self.get_category_by_id(p_id)
            result.append(category)
            if category.parent_id:
                parent = await get_categories(category.parent_id)
                result.extend(parent)
            
            return result
                        
        categories = await get_categories(filter.id)
        categories.reverse()
        
        return categories
                    
    async def get_categories_by_parent_id(
        self,
        parent_id: str | None = None,
        contains_danglings: bool = False,
    ) -> list[CategoryModel]:
        
        try:
            parent_id = convert_object_id(parent_id)
            if not parent_id and contains_danglings:
                valid_ids = await CategoryCollection.distinct("_id")        
                categories_list = await CategoryCollection.find_many(
                    Or(
                        CategoryCollection.parent_id == parent_id,
                        NotIn(CategoryCollection.parent_id, valid_ids),
                    ),
                ).to_list()
            else:
                categories_list = await CategoryCollection.find_many(
                    CategoryCollection.parent_id == parent_id,
                ).to_list()
                    
            return [ CategoryModel.model_validate(category, from_attributes=True) for category in categories_list ]
        except:
            raise EntityNotFoundError(status_code=404, message="Categories not found")
        
    async def get_categories_by_parent_id_listed(
        self,
        parent_id: str,
    ) -> list[CategoryModel]:
        
        async def get_categories(
            p_id: str | None = None,
        ) -> list[CategoryModel]:
            
            result: list[CategoryModel] = []
            categories = await self.get_categories_by_parent_id(p_id)
                        
            for c in categories:
                result.append(c)
                if c and c.parent_id:
                    result.extend(await get_categories(c.id))

            return result
                
        return await get_categories(parent_id)
    
    async def delete_categories_by_parent_id(
        self,
        parent_id: str,
    ) -> bool:
        try:
            parent_id = convert_object_id(parent_id)
            result = await CategoryCollection.find(
                CategoryCollection.parent_id == parent_id,
            ).delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="Categories not found")
        
    async def delete_all_categories(
        self,
    ) -> bool:
        try:
            result = await CategoryCollection.delete_all()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="Categories not found")