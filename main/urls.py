from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Redirect the homepage to /whats-on/
    path('', RedirectView.as_view(url='/whats-on/', permanent=False)),

    path('whats-on/', views.whats_on, name='whats_on'),
    path('project-modal/<slug:slug>/', views.project_modal, name='project_modal'),
    path('info/', views.info, name='info'),
]
