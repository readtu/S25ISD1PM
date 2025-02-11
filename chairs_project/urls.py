"""URL configuration for chairs_project project."""

from django.urls import include, path

urlpatterns = [
    path("", include("chairs_app.urls")),
]
