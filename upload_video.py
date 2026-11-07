import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PortFolio.settings")
django.setup()

import cloudinary.uploader
from django.conf import settings
from pathlib import Path

path = Path(settings.MEDIA_ROOT) / "projects/videos/Screen_Recording_2026-09-17_0317401.mp4"
print("Size (MB):", round(path.stat().st_size / 1_048_576, 1))

result = cloudinary.uploader.upload_large(
    str(path),
    resource_type="video",
    public_id="media/projects/videos/Screen_Recording_2026-09-17_0317401",
    chunk_size=6_000_000,
)
print(result["public_id"])