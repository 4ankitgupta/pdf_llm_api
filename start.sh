#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Start the web server in the background
uvicorn app.main:app --host 0.0.0.0 --port 10000 &

# Start the arq worker in the foreground
arq worker.WorkerSettings