from fastapi import FastAPI
from .database import create_db_and_tables
from .routes import email_router

async def lifespan(app):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(email_router, prefix="/generate", tags=["Email"])