from fastapi import FastAPI
from app.routes import document
from app.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PDF Processing API",
    description="An API to upload PDFs, extract info with an LLM, and fetch GitHub data synchronously.",
    version="1.0.0"
)

app.include_router(document.router, prefix="/api/documents", tags=["PDF Parser"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the PDF Parser API. Use /api/documents/upload to upload."}
