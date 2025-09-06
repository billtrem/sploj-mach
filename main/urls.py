from django.urls import path
from . import views

urlpatterns = [
    path("whats-on/", views.whats_on, name="whats_on"),
    path("project-modal/<slug:slug>/", views.project_modal, name="project_modal"),
    path("info/", views.info, name="info"),
]
