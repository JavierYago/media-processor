from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_UPLOAD_MB = 100
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024

ALLOWED_CONTENT_TYPES = {"video/mp4", "video/quicktime", "video/webm"}
ALLOWED_EXTENSIONS = {".mp4", ".mov", ".webm"}