import models
from access_token import artist_token_dependency
from db_dependency import db_dependency
from fastapi import APIRouter, status, HTTPException
from actions.response_model import ResponseMessage
from sqlalchemy import and_
from utills.check_ownership import is_document_owned_by_artist

router = APIRouter(tags=["Contributors"])


@router.post("/add-contributor", status_code=status.HTTP_201_CREATED)
async def like_episode(
        db: db_dependency,
        artist_id: int,
        contributing_artist_id : int,
        document_id: int,
):
    artist = db.query(models.Artists).where(models.Artists.Id == contributing_artist_id).first()

    # if access_token.id_ == artist.Id:
    #     raise HTTPException(404, "you cannot add yourself.")
    check = db.query(models.Contributors).where(
        and_(
            models.Contributors.OwnerId == artist_id,
            models.Contributors.ArtistId == artist.Id,
            models.Contributors.DocumentId == document_id,
        )
    ).first()

    if not artist:
        raise HTTPException(403, "an error occurred!")

    if check:
        raise HTTPException(403, f"the artist {artist.UserName} has already same contribution!")

    owned = await is_document_owned_by_artist(db, document_id=document_id, artist_id=artist_id)
    if owned:

        contributor = models.Contributors()
        contributor.OwnerId = artist_id
        contributor.ArtistId = artist.Id
        contributor.DocumentId = document_id

        db.add(contributor)
        db.commit()

        return ResponseMessage(error=False, message=f"the artist {artist.Name} added to document's contributors")
    else:
        raise HTTPException(404, "you dont own this document!")


@router.post("/delete-contributor", status_code=status.HTTP_201_CREATED)
async def like_episode(
        db: db_dependency,
        artist_id: int,
        contributor_id: int,
):
    contributor = db.query(models.Contributors).where(
        models.Contributors.Id == contributor_id
    ).first()
    if contributor and await is_document_owned_by_artist(
            db,
            document_id=contributor.DocumentId,
            artist_id=artist_id,
    ):
        db.delete(contributor)
        db.commit()
        return ResponseMessage(error=False, message="Contributor deleted!")
