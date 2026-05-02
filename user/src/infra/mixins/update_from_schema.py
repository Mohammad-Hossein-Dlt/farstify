from pydantic import BaseModel

class UpdateFromSchemaMixin:
    
    def update_from_schema(
        self,
        schema: BaseModel,
        exclude_unset: bool = True,
        exclude_none: bool = False
    ):
        data = schema.model_dump(exclude_unset=exclude_unset, exclude_none=exclude_none)
        
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        return self