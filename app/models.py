from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True, nullable=False)
    original_filename = Column(String, nullable=False)
    # Status can be: pending, processing, completed, failed
    status = Column(String, default="pending")
    company_name = Column(String, nullable=True)
    github_members = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    failure_reason = Column(String, nullable=True)