import re

from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.celery_app import celery_app
from app.config import OUTPUT_DIR, UPLOAD_DIR
from app.tasks import create_thumbnail_task

router = APIRouter(prefix="/jobs", tags=["jobs"])

STATE_MAP = {
    "PENDING": "pending",
    "STARTED": "processing",
    "SUCCESS": "completed",
    "FAILURE": "failed",
}


class ThumbnailJobRequest(BaseModel):
    file_id: str


@router.post("/thumbnail", status_code=202)
def create_thumbnail_job(body: ThumbnailJobRequest):
    if not re.fullmatch(r"[0-9a-f]{32}", body.file_id):
        raise HTTPException(status_code=400, detail="Identificador no válido")
    if not list(UPLOAD_DIR.glob(f"{body.file_id}.*")):
        raise HTTPException(status_code=404, detail="Vídeo no encontrado")

    result = create_thumbnail_task.delay(body.file_id)
    return {"job_id": result.id, "status": "pending"}


@router.get("/{job_id}")
def get_job(job_id: str):
    result = AsyncResult(job_id, app=celery_app)
    status = STATE_MAP.get(result.state, "processing")
    response = {"job_id": job_id, "status": status}
    if status == "failed":
        response["error"] = "No se pudo procesar el vídeo"
    return response


@router.get("/{job_id}/result")
def get_job_result(job_id: str):
    result = AsyncResult(job_id, app=celery_app)
    if result.state != "SUCCESS":
        raise HTTPException(status_code=409, detail="El trabajo aún no ha terminado")

    output = OUTPUT_DIR / result.result["output"]
    if not output.exists():
        raise HTTPException(status_code=404, detail="Resultado no disponible")
    return FileResponse(output, media_type="image/jpeg")