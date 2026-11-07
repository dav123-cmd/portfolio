import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PortFolio.settings")
django.setup()

from django.apps import apps
from django.db import models

# key = old path without extension, value = new Cloudinary name
MAP = {
    "blog/Blog1": "media/blog/Blog1_eim9nf",
    "blog/blog2": "media/blog/blog2_s1ahdy",
    "blog/blog3": "media/blog/blog3_ngw6i1",
    "profile/image_01": "media/profile/image_01_qx4auu",
    "profile/image_01_ABD85fr": "media/profile/image_01_ABD85fr_a72n7q",
    "projects/Annotation_2026-11-02_004719": "media/projects/Annotation_2026-11-02_004719_i98z4a",
    "projects/IMG-20260917-WA00201": "media/projects/IMG-20260917-WA00201_in2gka",
    "projects/sections/Annotation_2026-11-02_004719": "media/projects/sections/Annotation_2026-11-02_004719_xj2qzf",
    "projects/sections/Annotation_2026-11-02_004756": "media/projects/sections/Annotation_2026-11-02_004756_rjeqda",
    "projects/sections/IMG-20260917-WA00131": "media/projects/sections/IMG-20260917-WA00131_sbt3ou",
    "projects/sections/IMG-20260917-WA00151": "media/projects/sections/IMG-20260917-WA00151_qxnng1",
    "portfolio_media/image_01": "media/profile/image_01_qx4auu",
    "portfolio_media/image_01_ABD85fr": "media/profile/image_01_ABD85fr_a72n7q",
    "testimonials/AA1o3YVS1": "media/testimonials/AA1o3YVS1_z7fkkl",
    "testimonials/IMG-20260917-WA00171": "media/testimonials/IMG-20260917-WA00171_o5ym8t",
    "projects/videos/portfolio": "media/projects/videos/portfolio_efnp6n",
}

DRY_RUN = False  # set to False to actually save

for model in apps.get_models():
    for field in model._meta.get_fields():
        if not isinstance(field, models.FileField):
            continue
        for obj in model.objects.all():
            old = getattr(obj, field.name).name
            if not old:
                continue
            new = MAP.get(os.path.splitext(old)[0])
            if new:
                print(f"{model.__name__}#{obj.pk}.{field.name}: {old} -> {new}")
                if not DRY_RUN:
                    model.objects.filter(pk=obj.pk).update(**{field.name: new})
            else:
                print(f"NO MATCH {model.__name__}#{obj.pk}.{field.name}: {old}")