from pydantic import BaseModel
from typing import Literal

order_literal = Literal[
    "asc",  # sort values from lowest to highest
    "desc", # sort values from highest to lowest
]

class SortDirectionFilterInput(BaseModel):
    value: str | None = None
    order: order_literal = "asc"
