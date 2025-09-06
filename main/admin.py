from django.contrib import admin
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
        ('Images', {
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
    readonly_fields = ('created_at',)

    def poster_preview(self, obj):
        if obj.poster:
            return f'<img src="{obj.poster.url}" width="50" height="75" style="object-fit:cover; border-radius:4px;" />'
        return "—"
    poster_preview.allow_tags = True
    poster_preview.short_description = 'Poster'


@admin.register(InfoSection)
class InfoSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'project')
    search_fields = ('title', 'content')
