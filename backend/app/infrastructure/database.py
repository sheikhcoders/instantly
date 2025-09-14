from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
from backend.app.infrastructure.config import settings

class Database:
    client: AsyncIOMotorClient = None
    redis_client: redis.Redis = None

db = Database()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.DATABASE_URL)
    print(f"Connected to MongoDB at {settings.DATABASE_URL}")

async def close_mongo_connection():
    db.client.close()
    print("Closed MongoDB connection")

async def connect_to_redis():
    db.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    await db.redis_client.ping()
    print(f"Connected to Redis at {settings.REDIS_URL}")

async def close_redis_connection():
    await db.redis_client.close()
    print("Closed Redis connection")
