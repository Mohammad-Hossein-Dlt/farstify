from pydantic import BaseModel
from typing import TypeAlias, Literal

based_on_const: TypeAlias = Literal[
    "parent-id",
    "child-to-parent",
]

class CategoryFilterInput(BaseModel):
    id: int | str | None = None
    based_on: based_on_const = "parent-id"
    contains_danglings: bool = True