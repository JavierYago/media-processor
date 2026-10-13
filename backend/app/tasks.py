from app.celery_app import celery_app
from app.config import OUTPUT_DIR, THUMBNAIL_WIDTH, UPLOAD_DIR
from app.services.thumbnails import generate_thumbnail


@celery_app.task
def create_thumbnail_task(file_id: str) -> dict:
    matches = list(UPLOAD_DIR.glob(f"{file_id}.*"))
    if not matches:
        raise FileNotFoundError(f"No existe el vídeo {file_id}")

    output = OUTPUT_DIR / f"{file_id}.jpg"
    generate_thumbnail(matches[0], output, THUMBNAIL_WIDTH)
    return {"file_id": file_id, "output": output.name}