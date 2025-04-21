from django.contrib import admin
from .models import Post, ProjectCategory, InfoPage, Funder, TeamMember


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'display_categories')
    list_filter = ('categories', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}  # Auto-generate slug

    def display_categories(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()])
    display_categories.short_description = 'Categories'


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1
    show_change_link = True


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'signup_link', 'color')
    search_fields = ('name', 'info')
    inlines = [TeamMemberInline]


@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ('location',)
    inlines = [TeamMemberInline]


@admin.register(Funder)
class FunderAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_on_info_page')
    list_filter = ('show_on_info_page',)
    filter_horizontal = ('project_categories',)
    search_fields = ('name',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_title', 'project_category')
    list_filter = ('project_category',)
    search_fields = (
        'name',
        'job_title',
        'description',
        'project_category__name',
    )
