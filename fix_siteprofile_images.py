import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PortFolio.settings")
django.setup()

from Project_Hub.models import SiteProfile

profile = SiteProfile.objects.first()

if profile:
    if profile.hero_image:
        filename = str(profile.hero_image).split("/")[-1]
        profile.hero_image = f"portfolio_media/{filename}"

    if profile.about_image:
        filename = str(profile.about_image).split("/")[-1]
        profile.about_image = f"portfolio_media/{filename}"

    profile.save()

    print("SUCCESS! Images updated.")
    print("Hero:", profile.hero_image)
    print("About:", profile.about_image)

else:
    print("No SiteProfile record found.")