from django.urls import path
from . import views
from main.views import get_presigned_url

urlpatterns = [
    path('', views.whats_on, name='whats_on'),
    path('projects/<slug:category_slug>/', views.category_view, name='category_view'),
    path('info/', views.info, name='info'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('media-url/<path:key>/', get_presigned_url, name='get_presigned_url'),
]
