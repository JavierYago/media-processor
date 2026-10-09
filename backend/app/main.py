from fastapi import FastAPI
from app.routes import uploads

app = FastAPI(title="Media Processor")

app.include_router(uploads.router)

@app.get("/health")
def health():
    return {"status": "ok"}

