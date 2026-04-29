from fastapi import Depends
from sqlalchemy.orm import Session
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from .db_depend import db_client_depend

from src.repo.interface.Icategory_repo import ICategoryRepo
from src.repo.mongodb.category_mongodb_repo import CategoryMongodbRepo
   
def category_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> ICategoryRepo:
    
    # if isinstance(db_client, Session):
    #     return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return CategoryMongodbRepo()
