from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., min_length=2, max_length=30)
    username: str = Field(..., min_length=2, max_length=20)
    email: str
    hashed_password: str

class EmailLog(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user_input: str         # will define the user input
    reply_to: Optional[str] = Field(default=None)    # the email to reply to.
    context: Optional[str] = Field(default=None)
    length: Optional[int] = Field(default=None)  # the length of the response email.
    tone: str      # the tne of the email to be written.
    generated_email: str     # it will store the generated email.
    timestamp: str

