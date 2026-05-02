from pydantic import BaseModel

class UpdateUserInput(BaseModel):
    id: int | str
    name: str | None = None
    user_name: str | None = None