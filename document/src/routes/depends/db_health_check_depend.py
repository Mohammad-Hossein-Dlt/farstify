from fastapi import Depends
from .db_depend import db_client_depend
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from sqlalchemy.orm import Session
from sqlalchemy import text

async def db_health_check_depend(
    client: AsyncMongoClient | Session = Depends(db_client_depend)
):
    if isinstance(client, Session):
        try:
            request = client.execute(text("SELECT 1"))
            _ = request.scalar()
            return True
        except:
            client.rollback()
            return False
    
    if isinstance(client, AsyncMongoClient):
        try:
            await client.admin.command("ping")
            return True
        except:
            return False