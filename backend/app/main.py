from fastapi import FastAPI

app = FastAPI(title="Media Processor")


@app.get("/health")
def health():
    return {"status": "ok"}