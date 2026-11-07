from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.template.backends import django
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import (
    BlogCategory, BlogPost, ContactMessage, Project, Service, Skill, Testimonial,
)
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Import the CloudinaryImage and CloudinaryVideo methods for the simplified syntax used in this guide
from cloudinary import CloudinaryImage
from cloudinary import CloudinaryVideo
from .models import SiteProfile

def home(request):
    projects = list(
        Project.objects.filter(is_published=True)
        .prefetch_related("tags")
        .order_by("-is_featured", "order", "-created_at")[:3]
    )
    context = {
        "profile": SiteProfile.load(),
        "services": Service.objects.filter(is_active=True),
        "featured_project": projects[0] if projects else None,
        "other_projects": projects[1:],
        "skills": Skill.objects.all(),
        "testimonials": Testimonial.objects.filter(is_active=True)[:3],
        "latest_posts": BlogPost.objects.filter(is_published=True).select_related("category")[:3],
    }
    return render(request, "index.html", context)  # rename to your file


def project_list(request):
    published = Project.objects.filter(is_published=True)
    categories = (
        published.order_by("category")
        .values_list("category", flat=True)
        .distinct()
    )

    projects = published.prefetch_related("tags")
    active_category = request.GET.get("category", "").strip()
    if active_category:
        projects = projects.filter(category=active_category)

    context = {
        "projects": projects,
        "categories": categories,
        "active_category": active_category,
    }
    return render(request, "project_detail.html", context)

def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.filter(is_published=True)
        .prefetch_related("tags", "stats", "sections__items"),
        slug=slug,
    )
    context = {
        "project": project,
        "related_projects": project.get_related(),
    }
    return render(request, "case-study.html", context)


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True).select_related("category")

   
    active_category = request.GET.get("category", "").strip()
    if active_category:
        posts = posts.filter(category__slug=active_category)

   
    featured = posts.first()
    grid_posts = posts.exclude(pk=featured.pk) if featured else posts

    paginator = Paginator(grid_posts, 6)
    page_obj = paginator.get_page(request.GET.get("page"))
    page_range = paginator.get_elided_page_range(
        page_obj.number, on_each_side=1, on_ends=1
    )

    context = {
        "categories": BlogCategory.objects.all(),
        "active_category": active_category,
        "featured_post": featured if page_obj.number == 1 else None,
        "page_obj": page_obj,
        "posts": page_obj,
        "page_range": page_range,
        "ellipsis": paginator.ELLIPSIS,
        "category_qs": f"category={active_category}&" if active_category else "",
    }
    return render(request, "blog.html", context)


def blog_detail(request, slug):
    post = get_object_or_404(
        BlogPost.objects.filter(is_published=True).select_related("category"),
        slug=slug,
    )
    context = {
        "post": post,
        "related_posts": post.get_related(),
        "share_url": request.build_absolute_uri(),
    }
    return render(request, "blog-article.html", context)



@require_POST
def contact_submit(request):
    # Honeypot: real visitors never see or fill this field. Bots do.
    if request.POST.get("website"):
        return redirect(f"{reverse('portfolio:home')}#contact")

    name = request.POST.get("name", "").strip()[:100]
    email = request.POST.get("email", "").strip()
    subject = request.POST.get("subject", "").strip()[:150]
    message = request.POST.get("message", "").strip()

    try:
        validate_email(email)
    except ValidationError:
        email = ""

    if not (name and email and message):
        messages.error(request, "Please fill in your name, a valid email and a message.")
        return redirect(f"{reverse('portfolio:home')}#contact")

    ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)

    
    owner_email = SiteProfile.load().email
    if owner_email:
        send_mail(
            subject=f"[Portfolio] {subject or 'New message'} from {name}",
            message=f"From: {name} <{email}>\n\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[owner_email],
            fail_silently=True,
        )

    messages.success(request, "Thanks! I'll get back to you soon.")
    return redirect(f"{reverse('index')}#contact")
