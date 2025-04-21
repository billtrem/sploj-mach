from django.shortcuts import render, get_object_or_404
from .models import Post, ProjectCategory, InfoPage, Funder, TeamMember
from django.conf import settings
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_GET
import boto3


def whats_on(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'main/whats_on.html', {'posts': posts})


def category_view(request, category_slug):
    category = get_object_or_404(ProjectCategory, name__iexact=category_slug.replace('-', ' '))
    posts = Post.objects.filter(categories=category).order_by('-created_at')
    return render(request, 'main/category_view.html', {'category': category, 'posts': posts})


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
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'main/post_detail.html', {'post': post})


@require_GET
def get_presigned_url(request, key):
    s3 = boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    try:
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': key},
            ExpiresIn=3600  # 1 hour
        )
        return JsonResponse({'url': url})
    except Exception:
        raise Http404("File not found")
