import models
from fastapi import APIRouter, HTTPException, status
from db_dependency import db_dependency
from actions.response_model import ResponseMessage
from random import randint
from farapayamak import rest

router = APIRouter(tags=["Verify-Phone"])


@router.post("/verify-phone", status_code=status.HTTP_201_CREATED)
async def verify_user(
        db: db_dependency,
        phone: str,
):
    phone = phone.replace(" ", "")
    temp = db.query(models.UsersTemp).where(models.UsersTemp.Phone == phone).all()

    for t in temp:
        db.delete(t)

    db.commit()

    verify_code = randint(1000, 10000)

    rest_client = rest.Rest_Client('Hosein0098', '00316dce-bdbe-4f0f-821a-8673c0fb3f2d')
    result = rest_client.SendSMS(phone, '50004000890867', f'کد تایید شما: {verify_code}', False)

    if not result:
        raise HTTPException(404, "an error occurred!")

    temp = models.UsersTemp()
    temp.Phone = phone
    temp.VerifyCode = verify_code
    db.add(temp)
    db.commit()
    return ResponseMessage(error=False, message="Verify code has been set!")
