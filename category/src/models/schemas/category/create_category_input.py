from pydantic import BaseModel

class CreateCategoryInput(BaseModel):
    parent_id: int | str | None = None
    slug: str
    name: str