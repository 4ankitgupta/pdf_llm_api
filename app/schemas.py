from pydantic import BaseModel
from typing import List, Optional
import datetime

class DocumentResponse(BaseModel):
    id: int
    original_filename: str
    company_name: Optional[str] = None
    github_members: Optional[List[str]] = None
    timestamp: datetime.datetime

    class Config:
        from_attributes = True 