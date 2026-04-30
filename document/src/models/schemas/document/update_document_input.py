from pydantic import BaseModel

class UpdateDocumentInput(BaseModel):
    id: int | str
    title: str | None = None
    description: str | None = None
    single: bool | None = None
    active: bool | None = None