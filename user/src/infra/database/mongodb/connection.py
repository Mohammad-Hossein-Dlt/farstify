from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from .collections.user_collection import UserCollection
from .collections.user_image_collection import UserImageCollection
from .collections.user_link_collection import UserLinkCollection
from beanie import init_beanie


async def init_mongodb_client(
    host: str,
    port: int,
    username: str,
    password: str,
    db_name: str
) -> AsyncMongoClient:
    
    client = AsyncMongoClient(
        host=host,
        port=port,
        username=username,
        password=password,
    )
    
    database = AsyncDatabase(
        client=client,
        name=db_name,
    )
    
    await init_beanie(
        database=database,
        document_models=[
            UserCollection,
            UserImageCollection,
            UserLinkCollection,
        ],
    )
    
    return client