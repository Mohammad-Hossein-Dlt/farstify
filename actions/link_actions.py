from pydantic import BaseModel

class LinkData(BaseModel):
    Title: str | None = None
    Link: str | None = None