from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class StatusResponse(BaseModel):
    status: str
    message: Optional[str] = None


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

