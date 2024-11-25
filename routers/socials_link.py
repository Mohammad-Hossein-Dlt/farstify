import models
from fastapi import APIRouter, status
from db_dependency import db_dependency
from constants import Socials


router = APIRouter()


@router.post("/insert-social-link", status_code=status.HTTP_201_CREATED, tags=["SocialLink"])
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


@router.put("/update-single-social-link", status_code=status.HTTP_201_CREATED, tags=["SocialLink"])
async def update_single_social_link(
        db: db_dependency,
        link_id: int,
        title: str | None = None,
        social_type: Socials | None = None,
        link: str | None = None,
):
    if link_id is not None:
        the_link = db.query(models.SocialLink).where(models.SocialLink.Id == link_id).first()
        the_link.Title = title if title else the_link.Title
        the_link.ContentType = social_type if social_type else the_link.ContentType
        the_link.Link = link if link else the_link.Link
        db.commit()


@router.delete("/delete-social-link", status_code=status.HTTP_201_CREATED, tags=["SocialLink"])
async def delete_social_link(
        db: db_dependency,
        link_id: int,
):
    item = db.query(models.SocialLink).where(models.SocialLink.Id == link_id).first()
    if item:
        db.delete(item)
        db.commit()


@router.get("/fetch-all-socials-link", status_code=status.HTTP_201_CREATED, tags=["SocialLink"])
async def fetch_all_socials_link(db: db_dependency):
    return db.query(models.SocialLink).all()


@router.get("/fetch-single-social-link", status_code=status.HTTP_201_CREATED, tags=["SocialLink"])
async def fetch_single_social_link(
        db: db_dependency,
        link_id: int,
):
    return db.query(models.SocialLink).where(models.SocialLink.Id == link_id).first()
