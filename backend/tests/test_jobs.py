from app.routes import jobs


class FakeResult:
    id = "fake-job-id"


def test_job_rejects_invalid_id(client):
    response = client.post("/jobs/thumbnail", json={"file_id": "no-valido"})
    assert response.status_code == 400


def test_job_unknown_video(client):
    response = client.post("/jobs/thumbnail", json={"file_id": "0" * 32})
    assert response.status_code == 404


def test_job_is_enqueued(client, monkeypatch):
    # Sustituimos .delay para no necesitar Redis en los tests
    monkeypatch.setattr(
        jobs.create_thumbnail_task, "delay", lambda file_id: FakeResult()
    )
    upload = client.post(
        "/uploads",
        files={"file": ("clip.mp4", b"\x00" * 1024, "video/mp4")},
    )
    file_id = upload.json()["id"]

    response = client.post("/jobs/thumbnail", json={"file_id": file_id})

    assert response.status_code == 202
    assert response.json()["job_id"] == "fake-job-id"