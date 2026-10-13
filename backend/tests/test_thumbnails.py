import shutil
import subprocess

from app import tasks
import pytest

requires_ffmpeg = pytest.mark.skipif(
    shutil.which("ffmpeg") is None, reason="FFmpeg no instalado"
)


@pytest.fixture
def sample_video(tmp_path):
    path = tmp_path / "sample.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", "testsrc=duration=2:size=320x240:rate=10",
            "-pix_fmt", "yuv420p", str(path),
        ],
        check=True,
        capture_output=True,
    )
    return path


@requires_ffmpeg
def test_thumbnail_is_generated(client, sample_video):
    with sample_video.open("rb") as f:
        upload = client.post("/uploads", files={"file": ("sample.mp4", f, "video/mp4")})
    file_id = upload.json()["id"]

    response = client.post(f"/uploads/{file_id}/thumbnail")

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"


def test_thumbnail_unknown_id(client):
    response = client.post(f"/uploads/{'0' * 32}/thumbnail")
    assert response.status_code == 404


def test_thumbnail_invalid_id(client):
    response = client.post("/uploads/no-valido/thumbnail")
    assert response.status_code == 400

@requires_ffmpeg
def test_task_creates_thumbnail(client, sample_video):
    with sample_video.open("rb") as f:
        upload = client.post("/uploads", files={"file": ("sample.mp4", f, "video/mp4")})
    file_id = upload.json()["id"]

    result = tasks.create_thumbnail_task(file_id)

    assert result["file_id"] == file_id
    assert (tasks.OUTPUT_DIR / result["output"]).exists()