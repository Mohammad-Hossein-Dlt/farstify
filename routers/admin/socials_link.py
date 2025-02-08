from typing import List

import models
from fastapi import APIRouter, status, HTTPException

from actions.link_actions import get_link_data
from actions.response_model import ResponseMessage
from db_dependency import db_dependency
from constants import Socials
from utills.parse_null import pars_null

router = APIRouter(prefix="/admin/social_link", tags=["Admin-Social-Link"])


@router.post("/insert_social_link", status_code=status.HTTP_201_CREATED)
async def insert_social_link(
        db: db_dependency,
        link_id: int,
        title: str | None = None,
        social_type: Socials | None = None,
        url: str | None = None,
):
    title = pars_null(title)
    social_type = pars_null(social_type)
    url = pars_null(url)

    response = ResponseMessage(
        Error=False,
        Content={
            'Message': 'link added',
            'Link_Id': 0,
        },
    )

    if not link_id:
        new_link = models.SocialLinks()
        new_link.Title = title
        new_link.Type = social_type
        new_link.Url = url
        db.add(new_link)
        db.commit()

        response = ResponseMessage(
            Error=False,
            Content={
                'Message': 'link added',
                'Link_Id': new_link.Id,
            },
        )
    else:
        the_link = db.query(
            models.SocialLinks
        ).where(
            models.SocialLinks.Id == link_id
        ).first()

        if not the_link:
            raise HTTPException(404, "social link not found!")

        the_link.Title = title if title else the_link.Title
        the_link.ContentType = social_type if social_type else the_link.ContentType
        the_link.Url = url if url else the_link.Url
        db.commit()

        response = ResponseMessage(
            Error=False,
            Content={
                'Message': 'link edited',
                'Link_Id': the_link.Id,
            },
        )
    return response


@router.get("/fetch_all_socials_link", status_code=status.HTTP_201_CREATED)
async def fetch_all_socials_link(db: db_dependency):
    links = db.query(models.SocialLinks).all()
    return [get_link_data(link) for link in links]


@router.get("/fetch_single_social_link", status_code=status.HTTP_201_CREATED)
async def fetch_single_social_link(
        db: db_dependency,
        link_id: int,
):
    link = db.query(
        models.SocialLinks
    ).where(
        models.SocialLinks.Id == link_id
    ).first()

    if not link:
        raise HTTPException(404, 'link not found!')

    return get_link_data(link)


@router.put("/reorder_links", status_code=status.HTTP_200_OK)
async def reorder_images(
        db: db_dependency,
        links_id: List[int],
):
    links = db.query(
        models.SocialLinks
    ).all()

    for index, link_id in enumerate(links_id):
        for link in links:
            if link.Id == link_id:
                link.OrderBy = index

    db.commit()

    return ResponseMessage(error=False, message="images reordered!")


@router.delete("/delete_social_link", status_code=status.HTTP_201_CREATED)
async def delete_social_link(
        db: db_dependency,
        link_id: int,
):
    the_link = db.query(
        models.SocialLinks
    ).where(
        models.SocialLinks.Id == link_id
    ).first()

    if not the_link:
        raise HTTPException(404, "social link not found!")

    db.delete(the_link)
    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'link deleted',
        },
    )
