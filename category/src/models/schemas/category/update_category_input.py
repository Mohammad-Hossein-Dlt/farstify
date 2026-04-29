from pydantic import BaseModel

class UpdateCategoryInput(BaseModel):
    id: int | str
    parent_id: int | str | None = None
    slug: str | None = None
    name: str | None = None