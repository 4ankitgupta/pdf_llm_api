from fastapi import FastAPI
from app.routes import document

app = FastAPI(
    title="PDF Processing API",
    description="An API to upload PDFs, extract info with an LLM, and fetch GitHub data synchronously.",
    version="1.0.0"
)

app.include_router(document.router, prefix="/api/pdf", tags=["PDF Parser"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the PDF Parser API. Use /api/pdf/parse to upload."}
