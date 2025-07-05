from fastapi import APIRouter, File, UploadFile, HTTPException
from app.utils.pdf_parser import parse_pdf
from app.utils.llm_handler import extract_company_github_username
from app.utils.github_fetcher import get_organization_members

router = APIRouter()

@router.post("/upload")
async def parse_pdf_route(file: UploadFile = File(...)):
    file_content = await file.read()
    
    try:
        text_content = parse_pdf(file_content)
        if not text_content:
            raise HTTPException(status_code=422, detail="Could not extract text from PDF.")
        
        company_username = extract_company_github_username(text_content)
        if not company_username:
            raise HTTPException(status_code=422, detail="LLM could not identify a company GitHub username from the text.")
        
        github_members = get_organization_members(company_username)
        return(github_members)
        
    except Exception as e:
        return {"error": str(e)}
