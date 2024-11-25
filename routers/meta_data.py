from fastapi import APIRouter, status, Depends
from models import MetaData
from typing import Annotated
from pydantic import BaseModel
from db_dependency import db_dependency

router = APIRouter()


class MetaDataModel(BaseModel):
    MarketAppLink: str | None
    AboutUs: str | None
    ContactUs: str | None
    PrivacyAndTerms: str | None


@router.post("/update-metaData", status_code=status.HTTP_201_CREATED, tags=["Metadata"])
async def update_meta_data(
        db: db_dependency,
        meta_data: Annotated[MetaDataModel, Depends()]
):
    check = db.query(MetaData).count()
    if check == 0:
        item = MetaData(**meta_data.dict())
        db.add(item)
        db.commit()
    else:
        item = db.query(MetaData).first()
        item.MarketAppLink = meta_data.MarketAppLink
        item.AboutUs = meta_data.AboutUs
        item.ContactUs = meta_data.ContactUs
        item.PrivacyAndTerms = meta_data.PrivacyAndTerms
        db.commit()
