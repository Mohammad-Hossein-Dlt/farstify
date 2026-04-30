from pydantic import BaseModel

class CreateDocumentInput(BaseModel):
    title: str
    description: str
    single: bool = False
    active: bool = False