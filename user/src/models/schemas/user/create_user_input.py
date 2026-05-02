from pydantic import BaseModel

class CreateUserInput(BaseModel):
    name: str
    user_name: str