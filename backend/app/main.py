from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.interfaces.api.routes import router as api_router
from backend.app.infrastructure.database import connect_to_mongo, close_mongo_connection, connect_to_redis, close_redis_connection
from backend.app.core.config import settings
from backend.app.domain.models.base import User, Task, Session

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    await connect_to_redis()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()
    await close_redis_connection()

@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running"
    }
