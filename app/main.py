from fastapi import FastAPI
from .database import create_db_and_tables
from .routes.generate_email import email_router
from .routes.logs import logs_router

async def lifespan(app):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(email_router, prefix="/generate", tags=["Email"])
app.include_router(logs_router, prefix="/logs", tags=["Logs"])