import models
from fastapi import APIRouter, status, HTTPException
from actions.response_model import ResponseMessage
from db_dependency import db_dependency
from constants import Socials

router = APIRouter(prefix="/social_link", tags=["Social_Link"])


@router.post("/insert_social_link", status_code=status.HTTP_201_CREATED)
async def insert_social_link(
        db: db_dependency,
        title: str,
        social_type: Socials,
        link: str,
):
    item = models.SocialLink()
    item.Title = title
    item.Type = social_type
    item.Link = link
    db.add(item)
    db.commit()

    return ResponseMessage(error=False, message="link added")


@router.put("/update_single_social_link", status_code=status.HTTP_201_CREATED)
async def update_single_social_link(
        db: db_dependency,
        link_id: int,
        title: str | None = None,
        social_type: Socials | None = None,
        link: str | None = None,
):
    the_link = db.query(
        models.SocialLink
    ).where(
        models.SocialLink.Id == link_id
    ).first()

    if not the_link:
        raise HTTPException(404, "social link not found!")

    the_link.Title = title if title else the_link.Title
    the_link.ContentType = social_type if social_type else the_link.ContentType
    the_link.Link = link if link else the_link.Link
    db.commit()


@router.delete("/delete_social_link", status_code=status.HTTP_201_CREATED)
async def delete_social_link(
        db: db_dependency,
        link_id: int,
):
    the_link = db.query(
        models.SocialLink
    ).where(
        models.SocialLink.Id == link_id
    ).first()

    if not the_link:
        raise HTTPException(404, "social link not found!")

    if the_link:
        db.delete(the_link)
        db.commit()


@router.get("/fetch_all_socials_link", status_code=status.HTTP_201_CREATED)
async def fetch_all_socials_link(db: db_dependency):
    return db.query(models.SocialLink).all()


@router.get("/fetch_single_social_link", status_code=status.HTTP_201_CREATED)
async def fetch_single_social_link(
        db: db_dependency,
        link_id: int,
):
    return db.query(
        models.SocialLink
    ).where(
        models.SocialLink.Id == link_id
    ).first()
