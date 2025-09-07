from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Project, InfoSection


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_label', 'link', 'volunteer_label', 'volunteer_link', 'created_at', 'poster_preview')
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
        ('Main Button Settings', {
            'fields': ('link', 'link_label', 'color')
        }),
        ('Volunteer Button Settings', {
            'fields': ('volunteer_link', 'volunteer_label')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'poster_preview')

    def poster_preview(self, obj):
        if obj.poster and hasattr(obj.poster, 'url'):
            return mark_safe(
                f'<img src="{obj.poster.url}" width="50" height="75" '
                f'style="object-fit:cover; border-radius:4px;" />'
            )
        return "—"
    poster_preview.short_description = 'Poster'


@admin.register(InfoSection)
class InfoSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'is_links_section')
    search_fields = ('title', 'content')
    list_filter = ('is_links_section',)

    fieldsets = (
        (None, {
            'fields': ('title', 'project', 'content', 'image', 'is_links_section')
        }),
        ('Carousel Images (Optional – up to 20)', {
            'fields': tuple(f'carousel_image_{i}' for i in range(1, 21)),
            'classes': ('collapse',),
        }),
        ('Links (only if "Is links section" is checked)', {
            'fields': (
                ('link_1_label', 'link_1_url'),
                ('link_2_label', 'link_2_url'),
                ('link_3_label', 'link_3_url'),
                ('link_4_label', 'link_4_url'),
            ),
        }),
        ('Funder Logos', {
            'fields': (
                'funder_logo_1',
                'funder_logo_2',
                'funder_logo_3',
                'funder_logo_4',
            ),
        }),
    )
