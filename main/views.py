from django.shortcuts import render, get_object_or_404
from .models import Post, ProjectCategory, InfoPage, Funder, TeamMember
from django.conf import settings
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_GET
import boto3


def get_presigned_url_for_key(key):
    if not key:
        return ''
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
            ExpiresIn=3600
        )
        return url
    except Exception:
        return ''


def whats_on(request):
    posts = Post.objects.order_by('-created_at')
    for post in posts:
        if post.image:
            post.image_url = get_presigned_url_for_key(post.image.name)
    return render(request, 'main/whats_on.html', {'posts': posts})


def category_view(request, category_slug):
    category = get_object_or_404(ProjectCategory, name__iexact=category_slug.replace('-', ' '))
    if category.photo:
        category.photo_url = get_presigned_url_for_key(category.photo.name)

    if category.team_members.exists():
        for member in category.team_members.all():
            if member.photo:
                member.photo_url = get_presigned_url_for_key(member.photo.name)

    for funder in category.funders.all():
        if funder.logo:
            funder.logo_url = get_presigned_url_for_key(funder.logo.name)

    posts = Post.objects.filter(categories=category).order_by('-created_at')
    for post in posts:
        if post.image:
            post.image_url = get_presigned_url_for_key(post.image.name)

    return render(request, 'main/category_view.html', {
        'category': category,
        'posts': posts,
    })


def info(request):
    info_page = InfoPage.objects.first()
    funders = Funder.objects.all()
    team_members = TeamMember.objects.filter(info_page=info_page)

    for member in team_members:
        if member.photo:
            member.photo_url = get_presigned_url_for_key(member.photo.name)

    for funder in funders:
        if funder.logo:
            funder.logo_url = get_presigned_url_for_key(funder.logo.name)

    categories = ProjectCategory.objects.all()

    return render(request, 'main/info.html', {
        'info_page': info_page,
        'funders': funders,
        'categories': categories,
        'team_members': team_members,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.image:
        post.image_url = get_presigned_url_for_key(post.image.name)
    return render(request, 'main/post_detail.html', {'post': post})


@require_GET
def get_presigned_url(request, key):
    url = get_presigned_url_for_key(key)
    if url:
        return JsonResponse({'url': url})
    else:
        raise Http404("File not found")
