import uuid
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from arq.connections import ArqRedis, create_pool
from app import models, schemas
from app.database import get_db
from worker import WorkerSettings

router = APIRouter()
arq_pool: ArqRedis = None

@router.on_event("startup")
async def startup():
    global arq_pool
    arq_pool = await create_pool(WorkerSettings.redis_settings)

@router.on_event("shutdown")
async def shutdown():
    if arq_pool:
        await arq_pool.close()

async def get_arq_pool() -> ArqRedis:
    return arq_pool

@router.post("/upload", response_model=schemas.DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    arq_pool: ArqRedis = Depends(get_arq_pool)
):
    job_id = str(uuid.uuid4())
    file_content = await file.read()

    # Immediately create a record in the database
    new_doc = models.Document(
        job_id=job_id,
        original_filename=file.filename,
        status="pending"
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # Enqueue the background job
    await arq_pool.enqueue_job(
        "process_document_workflow",
        job_id,
        file.filename,
        file_content,
        _job_id=job_id
    )

    return schemas.DocumentUploadResponse(job_id=job_id)

@router.get("/status/{job_id}", response_model=schemas.DocumentStatusResponse)
async def get_document_status(job_id: str, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter(models.Document.job_id == job_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Job ID not found")
    return document