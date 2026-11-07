from django.contrib import admin
from .models import (
    SiteProfile, Service, Skill, Tag, Project, ProjectStat, ProjectSection,
    SectionItem, Testimonial, BlogCategory, BlogPost, ContactMessage,
)
@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False




@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_at", "is_published")
    list_filter = ("category", "is_published")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_highlighted", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author_name", "author_role", "rating", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read",)
    readonly_fields = ("name", "email", "subject", "message", "created_at")


admin.site.register([Skill, Tag, BlogCategory])




class ProjectStatInline(admin.TabularInline):
    model = ProjectStat
    extra = 3


class ProjectSectionInline(admin.StackedInline):
    model = ProjectSection
    extra = 1
    show_change_link = True 
    fields = ("kind", "title", "body", "image", "caption", "image_after", "caption_after", "order")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "has_video", "is_featured", "is_published", "order")
    list_editable = ("is_featured", "is_published", "order")
    list_filter = ("category", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    inlines = [ProjectStatInline, ProjectSectionInline]
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "tags", "summary")}),
        ("Media", {"fields": ("image", "demo_video")}),
        ("Links", {"fields": ("live_url", "repo_url")}),
        ("Details", {"fields": ("client", "role", "year", "duration", "timeline", "deliverables")}),
        ("Display", {"fields": ("is_featured", "is_published", "order")}),
    )

    @admin.display(boolean=True, description="Demo video")
    def has_video(self, obj):
        return bool(obj.demo_video)


class SectionItemInline(admin.TabularInline):
    model = SectionItem
    extra = 3


@admin.register(ProjectSection)
class ProjectSectionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "project", "kind", "order")
    list_filter = ("project", "kind")
    inlines = [SectionItemInline]