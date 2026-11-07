import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PortFolio.settings")
django.setup()

from pathlib import Path
from django.conf import settings
from django.core.files import File
from cloudinary_storage.storage import MediaCloudinaryStorage, VideoMediaCloudinaryStorage

VIDEO_EXT = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
image_storage = MediaCloudinaryStorage()
video_storage = VideoMediaCloudinaryStorage()

media_root = Path(settings.MEDIA_ROOT)

for path in sorted(media_root.rglob("*")):
    if not path.is_file():
        continue
    name = path.relative_to(media_root).as_posix()   # e.g. blog/blog3.jfif
    storage = video_storage if path.suffix.lower() in VIDEO_EXT else image_storage
    try:
        with open(path, "rb") as f:
            saved = storage.save(name, File(f))
        print(f"OK   {name} -> {saved}")
    except Exception as e:
        print(f"FAIL {name}: {e}")