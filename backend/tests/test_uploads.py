def test_upload_rejects_non_video(client):
    response = client.post(
        "/uploads",
        files={"file": ("notas.txt", b"hola", "text/plain")},
    )
    assert response.status_code == 415


def test_upload_accepts_small_video(client):
    response = client.post(
        "/uploads",
        files={"file": ("clip.mp4", b"\x00" * 1024, "video/mp4")},
    )
    assert response.status_code == 201
    assert "id" in response.json()