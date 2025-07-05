from fastapi import APIRouter, File, UploadFile
from app.utils.pdf_parser import parse_pdf

router = APIRouter()

@router.post("/parse")
async def parse_pdf_route(file: UploadFile = File(...)):
    file_content = await file.read()
    
    try:
        text = parse_pdf(file_content)
        print("\n\n--- Extracted PDF Text ---\n")
        print(text)
        return {"message": "PDF content printed in terminal"}
    except Exception as e:
        return {"error": str(e)}
