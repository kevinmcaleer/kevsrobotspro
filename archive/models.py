from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

# Pydantic models for request bodies
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Like(BaseModel):
    username: str
    page_id: str

class Comment(BaseModel):
    username: str
    page_id: str
    content: str
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
