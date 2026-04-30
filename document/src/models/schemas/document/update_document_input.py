from pydantic import BaseModel

class UpdateDocumentInput(BaseModel):
    id: int | str
    name: str | None = None
    description: str | None = None
    active: bool | None = None