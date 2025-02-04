from fastapi import APIRouter, HTTPException, Depends
from ..schemas import EmailLogRead
from ..crud import crud_email_log
from ..database import get_session

logs_router = APIRouter()


@logs_router.get("/")
async def get_logs(db = Depends(get_session)):
    logs = await crud_email_log.get_multi(db=db)
    if not logs:
        raise HTTPException(status_code=404, detail="Logs not found")
    return logs


@logs_router.get("/{id}", response_model=EmailLogRead)
async def get_log(id: int, db = Depends(get_session)):
    log = await crud_email_log.get(db=db, id=id)

    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    else:
        return log

