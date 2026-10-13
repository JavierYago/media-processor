from fastapi import FastAPI
from .routes import uploads
from app.routes import jobs

app = FastAPI(title="Media Processor")

app.include_router(uploads.router)
app.include_router(jobs.router)

@app.get("/health")
def health():
    return {"status": "ok"}

