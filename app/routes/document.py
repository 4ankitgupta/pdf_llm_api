from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from app.utils.pdf_parser import parse_pdf
from app.utils.llm_handler import extract_company_github_username
from app.utils.github_fetcher import get_organization_members

from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/upload", response_model=schemas.DocumentResponse)
async def parse_pdf_route(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    file_content = await file.read()
    
    try:
        text_content = parse_pdf(file_content)
        if not text_content:
            raise HTTPException(status_code=422, detail="Could not extract text from PDF.")
        
        company_username = extract_company_github_username(text_content)
        if not company_username:
            raise HTTPException(status_code=422, detail="LLM could not identify a company GitHub username from the text.")
        
        github_members = get_organization_members(company_username)
        
        
        new_document = models.Document(
            original_filename=file.filename,
            company_name=company_username,
            github_members=github_members if github_members is not None else []
        )
        db.add(new_document)
        db.commit()
        db.refresh(new_document)

        return new_document
        
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")
