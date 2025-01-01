from typing import Any

from pydantic import BaseModel


class ResponseMessage(BaseModel):
    error: bool = True
    message: Any = "an error occurred!"
