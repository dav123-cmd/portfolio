# portfolio/context_processors.py
from django.urls import reverse

from .models import SiteProfile


def site_profile(request):
    home = reverse("portfolio:home")
    current = getattr(request.resolver_match, "url_name", None)

    
    links = [
        ("Services", "services", ()),
        ("Work", "work", ("projects", "project_detail")),
        ("About", "about", ()),
        ("Reviews", "reviews", ()),
        ("Blog", "blog", ("blog", "blog_detail")),
        ("Contact", "contact", ()),
    ]
    nav_links = [
        {
            "label": label,
            "key": key,
            "url": f"{home}#{key}",
            "page_active": current in pages,
        }
        for label, key, pages in links
    ]

    return {
        "profile": SiteProfile.load(),
        "nav_links": nav_links,
        "home_url": home,
    }