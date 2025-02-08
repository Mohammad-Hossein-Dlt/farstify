import models
from pydantic import BaseModel


class LinkData(BaseModel):
    Id: int | None = None
    ArtistId: int | None = None
    Title: str | None = None
    Url: str | None = None
    Type: str | None = None
    OrderBy: int | None = None


def get_link_data(
        link: models.ArtistLinks,
) -> LinkData:

    data = LinkData()

    data.Id = link.Id
    data.ArtistId = link.ArtistId
    data.Title = link.Title
    data.Url = link.Url
    data.OrderBy = link.OrderBy
    data.Type = link.Type

    return  data
