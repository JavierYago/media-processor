import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import (
    ALLOWED_CONTENT_TYPES,
    ALLOWED_EXTENSIONS,
    MAX_UPLOAD_BYTES,
    UPLOAD_DIR,
)

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("", status_code=201)
async def upload_video(file: UploadFile = File(...)):
    extension = Path(file.filename or "").suffix.lower()

    if file.content_type not in ALLOWED_CONTENT_TYPES or extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Tipo de archivo no permitido")

    file_id = uuid.uuid4().hex
    destination = UPLOAD_DIR / f"{file_id}{extension}"

    size = 0
    with destination.open("wb") as out:
        while chunk := await file.read(1024 * 1024):  # 1 MB por trozo
            size += len(chunk)
            if size > MAX_UPLOAD_BYTES:
                out.close()
                destination.unlink(missing_ok=True)
                raise HTTPException(status_code=413, detail="Archivo demasiado grande")
            out.write(chunk)

    return {"id": file_id, "filename": file.filename, "size_bytes": size}