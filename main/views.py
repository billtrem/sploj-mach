from django.shortcuts import render, get_object_or_404
from .models import Post, ProjectCategory, InfoPage, Funder, TeamMember

def whats_on(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'main/whats_on.html', {'posts': posts})

def category_view(request, category_slug):
    category = get_object_or_404(ProjectCategory, name__iexact=category_slug.replace('-', ' '))
    posts = Post.objects.filter(categories=category).order_by('-created_at')
    return render(request, 'main/category_view.html', {'category': category, 'posts': posts})


def info(request):
    # Get the info page
    info_page = InfoPage.objects.first()
    
    # Get team members associated with the info page
    team_members = TeamMember.objects.filter(info_page=info_page)

    # Get categories for the dropdown in the contact form
    categories = ProjectCategory.objects.all()

    context = {
        'info_page': info_page,
        'team_members': team_members,
        'categories': categories,
    }

    return render(request, 'main/info.html', context)


def info(request):
    info_page = InfoPage.objects.first()
    funders = Funder.objects.all()
    team_members = TeamMember.objects.filter(info_page=info_page)
    categories = ProjectCategory.objects.all()
    return render(request, 'main/info.html', {
        'info_page': info_page,
        'funders': funders,
        'categories': categories,
        'team_members': team_members,
    })


def post_detail(request, slug):
    # Get the post by slug or return a 404 error if not found
    post = get_object_or_404(Post, slug=slug)
    
    context = {
        'post': post,
    }
    
    return render(request, 'main/post_detail.html', context)