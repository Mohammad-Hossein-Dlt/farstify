from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from beanie import init_beanie

from .collections.user.user_collection import UserCollection
from .collections.user.user_image_collection import UserImageCollection
from .collections.user.user_link_collection import UserLinkCollection
from .collections.follow.follows import FollowsCollection

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
            FollowsCollection,
        ],
    )
    
    return client