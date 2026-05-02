from pydantic import BaseModel, model_validator
from typing import Literal, Self

order_literal = Literal[
    "asc",  # sort values from lowest to highest
    "desc", # sort values from highest to lowest
]

class BaseFilterCriteria(BaseModel):
    order: order_literal = "asc"
    page: int | None = None
    limit: int | None = None
    

    @model_validator(mode='after')
    def validate_values(
        self
    ) -> Self:
        
        if not self.page:
            self.page = 0
        
        if not self.limit:
            self.limit = 0
        
        return self