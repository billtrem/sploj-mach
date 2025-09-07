from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Project, InfoSection


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_label', 'link', 'created_at', 'poster_preview')
    search_fields = ('title', 'description')
    list_filter = ('link_label', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description')
        }),
        ('Images (Stored on Cloudinary)', {
            'fields': ('poster', 'horizontal_image')
        }),
        ('Video', {
            'fields': ('video_embed_code',)
        }),
        ('Link Settings', {
            'fields': ('link', 'link_label', 'color')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'poster_preview')

    def poster_preview(self, obj):
        """Show a small preview of the poster in admin list."""
        if obj.poster and hasattr(obj.poster, 'url'):
            return mark_safe(
                f'<img src="{obj.poster.url}" width="50" height="75" '
                f'style="object-fit:cover; border-radius:4px;" />'
            )
        return "—"

    poster_preview.short_description = 'Poster'


@admin.register(InfoSection)
class InfoSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'project')
    search_fields = ('title', 'content')
