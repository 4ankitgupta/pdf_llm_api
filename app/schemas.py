from pydantic import BaseModel
from typing import List, Optional
import datetime

class DocumentUploadResponse(BaseModel):
    job_id: str

class DocumentStatusResponse(BaseModel):
    job_id: str
    status: str
    original_filename: str
    company_name: Optional[str] = None
    github_members: Optional[List[str]] = None
    timestamp: datetime.datetime
    failure_reason: Optional[str] = None

    class Config:
        from_attributes = True