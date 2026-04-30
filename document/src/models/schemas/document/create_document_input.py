from pydantic import BaseModel

class CreateDocumentInput(BaseModel):
    name: str
    description: str
    active: bool = False