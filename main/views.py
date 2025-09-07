from django.shortcuts import render, get_object_or_404
from .models import Project, InfoSection


def whats_on(request):
    projects = Project.objects.order_by('-created_at')
    return render(request, 'main/whats_on.html', {
        'projects': projects
    })


def project_modal(request, slug):
    project = get_object_or_404(Project, slug=slug)
    sections = project.info_sections.all().order_by('id')

    if project.link_label == 'signup':
        button_color = '#000000'
    else:
        button_color = project.color or '#000000'

    return render(request, 'main/projectdetail.html', {
        'project': project,
        'sections': sections,
        'button_color': button_color
    })


def info(request):
    sections = InfoSection.objects.filter(project__isnull=True).order_by('id')

    # Top image from the first section that has one
    top_image = None
    if sections.exists():
        first_with_image = next((s for s in sections if s.image), None)
        if first_with_image:
            top_image = first_with_image.image

    # All important links sections
    link_sections = [s for s in sections if s.is_links_section]

    return render(request, 'main/info.html', {
        'sections': sections,
        'top_image': top_image,
        'link_sections': link_sections
    })
