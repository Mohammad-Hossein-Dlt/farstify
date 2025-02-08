from fastapi import APIRouter, status, Depends
from models import MetaData
from typing import Annotated
from pydantic import BaseModel
from db_dependency import db_dependency

router = APIRouter(prefix="/admin/meta_data", tags=["Admin-MetaData"])


class MetaDataModel(BaseModel):
    MarketAppLink: str | None
    AboutUs: str | None
    ContactUs: str | None
    PrivacyAndTerms: str | None


@router.post("/edit_meta_data", status_code=status.HTTP_201_CREATED)
async def edit_meta_data(
        db: db_dependency,
        meta_data: Annotated[MetaDataModel, Depends()]
):
    check = db.query(MetaData).count()

    if check == 0:

        item = MetaData()

        item.MarketAppLink = meta_data.MarketAppLink
        item.AboutUs = meta_data.AboutUs
        item.ContactUs = meta_data.ContactUs
        item.PrivacyAndTerms = meta_data.PrivacyAndTerms

        db.add(item)
        db.commit()

    else:
        item = db.query(MetaData).first()
        item.MarketAppLink = meta_data.MarketAppLink
        item.AboutUs = meta_data.AboutUs
        item.ContactUs = meta_data.ContactUs
        item.PrivacyAndTerms = meta_data.PrivacyAndTerms
        db.commit()
