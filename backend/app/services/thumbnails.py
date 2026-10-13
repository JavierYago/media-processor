import subprocess
from pathlib import Path


class ThumbnailError(Exception):
    pass


def generate_thumbnail(video_path: Path, output_path: Path, width: int = 320) -> None:
    # Probamos en el segundo 1; si el vídeo es más corto, caemos al segundo 0
    for second in ("1", "0"):
        command = [
            "ffmpeg", "-y",
            "-ss", second,
            "-i", str(video_path),
            "-frames:v", "1",
            "-vf", f"scale={width}:-1",
            str(output_path),
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        except FileNotFoundError as exc:
            raise ThumbnailError("FFmpeg no está instalado") from exc
        except subprocess.TimeoutExpired as exc:
            raise ThumbnailError("FFmpeg tardó demasiado") from exc

        if result.returncode == 0 and output_path.exists():
            return

    raise ThumbnailError(result.stderr[-500:])