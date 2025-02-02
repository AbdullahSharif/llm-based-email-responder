from datetime import datetime, timezone

from typing import Optional
from sqlmodel import SQLModel, Field

class UserCreate(SQLModel):
    name: str
    username: str
    email: str
    password: str

class UserRead(SQLModel):
    id: int
    name: str
    username: str
    email: str

class UserCreateInternal(SQLModel):
    name: str
    username: str
    email: str
    hashed_password: str

# -------email request--------
class EmailRequest(SQLModel):
    user_id: int
    user_input: str
    reply_to : Optional[str] = Field(default=None)
    context: Optional[str] = Field(default=None)
    length: Optional[int] = Field(default=None)
    tone: str


# ------- email response--------
class EmailResponse(SQLModel):
    generated_email: str


# --------- For internal manipulation --------
class EmailLogCreate(SQLModel):
    user_id: int
    user_input: str
    reply_to : Optional[str] = Field(default=None)
    context: Optional[str] = Field(default=None)
    length: Optional[int] = Field(default=None)
    tone: str
    generated_email: str
    timestamp: datetime = Field(
        default_factory=lambda: str(datetime.now(tz=timezone.utc))
    )


class EmailLogRead(SQLModel):
    user_id: int
    user_input: str
    reply_to : Optional[str] = Field(default=None)
    context: Optional[str] = Field(default=None)
    length: Optional[int] = Field(default=None)
    tone: str
    generated_email: str
    timestamp: str



