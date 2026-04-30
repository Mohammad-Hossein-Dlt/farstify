from pydantic import BaseModel

class CreateImageInput(BaseModel):
    document_id: str
    is_main: bool = False