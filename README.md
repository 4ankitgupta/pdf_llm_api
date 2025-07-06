# 📄 PDF Processing & GitHub Info Extractor API

A robust backend API service designed to process PDF documents, extract information using a Large Language Model (LLM), fetch supplementary data from the GitHub API, and persist the results.

**Live Deployment**: [https://pdf-llm-service.onrender.com](https://pdf-llm-service.onrender.com)

---

## 🚀 Features

- **📤 PDF Upload**: Upload endpoint for PDF files.
- **🔁 Asynchronous Processing**: Uses background tasks for non-blocking PDF processing.
- **📝 Text Extraction**: Extracts text content from uploaded PDFs.
- **🤖 LLM Integration**: Uses Groq’s Llama 3 to identify GitHub org usernames from the PDF.
- **🐙 GitHub API Integration**: Retrieves public members of the identified GitHub organization.
- **🗃️ Data Persistence**: Stores job data including status, results, and timestamps in SQLite.
- **📊 Job Status Tracking**: Check the status of a processing job anytime.

---

## 🧰 Tech Stack

- **Backend Framework**: FastAPI
- **Task Queue**: ARQ (Async Redis Queue)
- **Database**: SQLite with SQLAlchemy
- **PDF Parsing**: pdfplumber
- **LLM**: Groq (Llama 3)
- **HTTP Requests**: requests
- **Deployment**: Render (Web Service + Redis)

---

## 📡 API Endpoints

### 1. Upload a PDF for Processing

- **URL**: `POST /api/documents/upload`  
- **Request Body**: `multipart/form-data` with key `file`
- **Response**:
```json
{
  "job_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
}
```

## 📥 GET /api/documents/status/{job_id}

This endpoint allows you to check the status and results of a previously submitted PDF processing job.

### 🔗 URL


Replace `{job_id}` with the actual job ID returned from the PDF upload response.

### 🔄 Example using cURL

```bash
curl -X GET \
  https://pdf-llm-service.onrender.com/api/documents/status/a1b2c3d4-e5f6-7890-1234-567890abcdef
```

✅ Possible Responses
🟡 Job is still processing
```json
{
  "job_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "status": "processing",
  "original_filename": "document.pdf",
  "company_name": null,
  "github_members": null,
  "timestamp": "2023-10-27T10:30:00.123456+00:00",
  "failure_reason": null
}
```

❌ Failed

```json
{
  "job_id": "...",
  "status": "failed",
  "original_filename": "document.pdf",
  "company_name": null,
  "github_members": null,
  "timestamp": "2023-10-27T10:30:00.123456+00:00",
  "failure_reason": "LLM could not identify a company GitHub username."
}
```

🛠️ Local Setup & Installation
1. Clone the Repo
```bash
git clone https://github.com/4ankitgupta/pdf_llm_api.git
cd pdf-llm-api
```
2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Environment Variables
Create a .env file in the root directory:

```ini
GROQ_API_KEY="YOUR_GROQ_API_KEY"
```
5. Start Redis
Ensure Redis is running locally on port 6379.

Use Docker:

```bash
docker run -d -p 6379:6379 redis
```
6. Run the Application
Terminal 1: Start background worker

```bash
arq worker.WorkerSettings
```
Terminal 2: Start FastAPI server

```bash
uvicorn app.main:app --reload
```
The server will run at: http://127.0.0.1:8000
