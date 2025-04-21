from django.urls import path
from . import views

urlpatterns = [
    # Main site pages
    path('', views.whats_on, name='whats_on'),
    path('projects/<slug:category_slug>/', views.category_view, name='category_view'),
    path('info/', views.info, name='info'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),

    # Wasabi Pre-signed URL route (used for secure image access)
    path('media-url/<path:key>/', views.get_presigned_url, name='get_presigned_url'),
]
