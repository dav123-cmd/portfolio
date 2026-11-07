from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
import math
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import cloudinary
import cloudinary.uploader
import cloudinary.api
# Import the CloudinaryImage and CloudinaryVideo methods for the simplified syntax used in this guide
from cloudinary import CloudinaryImage
from cloudinary import CloudinaryVideo

class SiteProfile(models.Model):
    """Single row holding all the 'about me' and hero data."""
    full_name = models.CharField(max_length=100, default="David")
    short_name = models.CharField(max_length=50, default="DAVID", help_text="Shown in the hero: Hi, I'm ...")
    role = models.CharField(max_length=100, default="Full Stack Developer")
    tagline = models.CharField(max_length=255, default="I design and build digital products that people love to use.")
    availability_text = models.CharField(max_length=60, default="Available for work")
    badge_text = models.CharField(max_length=60, default="Open to projects")
    is_available = models.BooleanField(default=True)
    hero_image = models.ImageField(upload_to="profile/", blank=True)
    about_image = models.ImageField(upload_to="profile/", blank=True)
    about_heading = models.CharField(max_length=120, default="A bit about who I am")
    about_paragraph_1 = models.TextField()
    about_paragraph_2 = models.TextField(blank=True)
    projects_done = models.PositiveIntegerField(default=0)
    happy_clients = models.PositiveIntegerField(default=0)
    years_experience = models.PositiveIntegerField(default=0)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=100, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site profile"
        verbose_name_plural = "Site profile"

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce singleton
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(
            pk=1, defaults={"about_paragraph_1": "Tell visitors about yourself."}
        )
        return obj

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_svg = models.TextField(
        blank=True,
        help_text="Inner SVG markup, e.g. <path stroke-linecap='round' stroke-width='2' d='...'/>",
    )
    is_highlighted = models.BooleanField(default=False, help_text="Dark featured card")
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

class Skill(models.Model):
    name = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    category = models.CharField(max_length=60, help_text="Badge shown first, e.g. SaaS, Fintech")
    tags = models.ManyToManyField(Tag, blank=True, related_name="projects")
    summary = models.TextField(help_text="Short text for cards")
    image = models.ImageField(upload_to="projects/", blank=True)
    demo_video=models.FileField(
        upload_to="projects/videos/",
        blank=True
    )
    client = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    duration = models.CharField(max_length=50, blank=True, help_text="e.g. 6 weeks")
    timeline = models.CharField(max_length=60, blank=True, help_text="e.g. Jan – Feb 2025")
    deliverables = models.CharField(max_length=150, blank=True, help_text="e.g. Figma, HTML/CSS")
    live_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def get_related(self, limit=3):
        """Same-category projects first, then the latest others."""
        qs = (Project.objects.filter(is_published=True)
              .exclude(pk=self.pk).prefetch_related("tags"))
        related = list(qs.filter(category=self.category)[:limit])
        if len(related) < limit:
            ids = [p.pk for p in related]
            related += list(qs.exclude(pk__in=ids)[: limit - len(related)])
        return related

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

class ProjectStat(models.Model):
    """Results banner: big number + label."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="stats")
    value = models.CharField(max_length=20, help_text="e.g. −40%, +27%, 4.8/5")
    label = models.CharField(max_length=80)
    is_highlighted = models.BooleanField(default=False, help_text="Show the number in the accent colour")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value} {self.label}"

class ProjectSection(models.Model):
    TEXT = "text"
    PRINCIPLES = "principles"
    STEPS = "steps"
    IMAGE = "image"
    COMPARE = "compare"
    KIND_CHOICES = [
        (TEXT, "Text"),
        (PRINCIPLES, "Cards grid (e.g. design principles)"),
        (STEPS, "Numbered steps (e.g. process)"),
        (IMAGE, "Full-width image"),
        (COMPARE, "Before / after images"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="sections")
    kind = models.CharField(max_length=12, choices=KIND_CHOICES, default=TEXT)
    title = models.CharField(max_length=150, blank=True, help_text="Shown as an H2 (Text / Cards / Steps)")
    body = models.TextField(blank=True, help_text="HTML: <p>, <h3>, <ul>, <blockquote>...")
    image = models.ImageField(upload_to="projects/sections/", blank=True,
                              help_text="Image, or the 'before' image for Before / after")
    caption = models.CharField(max_length=200, blank=True)
    image_after = models.ImageField(upload_to="projects/sections/", blank=True, help_text="'After' image")
    caption_after = models.CharField(max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.project.title} · {self.get_kind_display()} · {self.title or self.pk}"

class SectionItem(models.Model):
    """Cards (principles) or steps inside a section."""
    section = models.ForeignKey(ProjectSection, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=120)
    description = models.TextField()
    icon_svg = models.TextField(blank=True, help_text="Inner SVG markup (cards grid only)")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

def validate_video_size(f):
    if f.size > 100 * 1024 * 1024:
        raise ValidationError("Video must be 100 MB or smaller.")

class Testimonial(models.Model):
    quote = models.TextField()
    author_name = models.CharField(max_length=100)
    author_role = models.CharField(max_length=100, help_text="e.g. CPO, Novu")
    avatar = models.ImageField(upload_to="testimonials/", blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    is_highlighted = models.BooleanField(default=False, help_text="Dark card")
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    @property
    def stars(self):
        return range(max(0, min(self.rating, 5)))

    def __str__(self):
        return f"{self.author_name} ({self.author_role})"


class BlogCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Blog categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210, unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name="posts")
    excerpt = models.CharField(max_length=300)
    content = models.TextField()
    cover_image = models.ImageField(upload_to="blog/", blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:blog_detail", kwargs={"slug": self.slug})

    @property
    def reading_time(self):
        words = len(strip_tags(self.content).split())
        return max(1, math.ceil(words / 200))

    def get_related(self, limit=3):
        """Same-category posts first, then fill up with the latest others."""
        qs = (BlogPost.objects.filter(is_published=True)
              .exclude(pk=self.pk).select_related("category"))
        related = list(qs.filter(category=self.category)[:limit]) if self.category_id else []
        if len(related) < limit:
            ids = [p.pk for p in related]
            related += list(qs.exclude(pk__in=ids)[: limit - len(related)])
        return related

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}: {self.subject or self.message[:30]}"