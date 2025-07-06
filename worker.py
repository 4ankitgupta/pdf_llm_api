import os
import asyncio
import random
from app.database import SessionLocal
from app.models import Document
from app.utils.pdf_parser import parse_pdf
from app.utils.llm_handler import extract_company_github_username
from app.utils.github_fetcher import get_organization_members
from sqlalchemy.orm import Session
import redis.asyncio as redis
from arq.connections import RedisSettings

from dotenv import load_dotenv
load_dotenv()

async def process_document_workflow(ctx, job_id: str, filename: str, file_content: bytes):
    """The main background task that processes the uploaded PDF."""
    db: Session = SessionLocal()
    doc = db.query(Document).filter(Document.job_id == job_id).first()
    if not doc:
        print(f"Job {job_id}: Document not found in DB.")
        return

    try:
        doc.status = "processing"
        db.commit()
        db.refresh(doc)
        print(f"Job {job_id}: Started processing for '{filename}'.")

        delay = random.randint(30, 60)
        print(f"Job {job_id}: Simulating long task for {delay} seconds...")
        await asyncio.sleep(delay)

        # Parse PDF
        text_content = parse_pdf(file_content)
        if not text_content:
            raise ValueError("Failed to extract any text from the PDF.")

        # LLM Integration
        company_username = extract_company_github_username(text_content)
        if not company_username:
            raise ValueError("LLM could not identify a company GitHub username.")
        doc.company_name = company_username
        db.commit()
        print(f"Job {job_id}: LLM identified company: '{company_username}'.")

        # GitHub API Call
        github_members = get_organization_members(company_username)
        if github_members is None:
            doc.github_members = []
        else:
            doc.github_members = github_members
        print(f"Job {job_id}: Found {len(doc.github_members)} members for '{company_username}'.")

        # Finalize
        doc.status = "completed"
        print(f"Job {job_id}: Processing completed successfully.")

    except Exception as e:
        print(f"Job {job_id}: FAILED. Reason: {e}")
        if 'doc' in locals() and db.query(Document).get(doc.id):
            doc.status = "failed"
            doc.failure_reason = str(e)
    finally:
        db.commit()
        db.close()
        print(f"Job {job_id}: DB session closed.")

class WorkerSettings:
    functions = [process_document_workflow]
    redis_settings = RedisSettings.from_dsn(os.getenv("REDIS_URL", 'redis://localhost:6379'))