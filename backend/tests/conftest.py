import pytest
from fastapi.testclient import TestClient

from app import tasks
from app.main import app
from app.routes import jobs, uploads


@pytest.fixture
def client(tmp_path, monkeypatch):
    upload_dir = tmp_path / "uploads"
    output_dir = tmp_path / "outputs"
    upload_dir.mkdir()
    output_dir.mkdir()

    # Redirigimos las carpetas a temporales solo durante el test. Cada módulo
    # importó sus propias referencias desde app.config.
    monkeypatch.setattr(uploads, "UPLOAD_DIR", upload_dir)
    monkeypatch.setattr(jobs, "UPLOAD_DIR", upload_dir)
    monkeypatch.setattr(jobs, "OUTPUT_DIR", output_dir)
    monkeypatch.setattr(tasks, "UPLOAD_DIR", upload_dir)
    monkeypatch.setattr(tasks, "OUTPUT_DIR", output_dir)

    return TestClient(app)