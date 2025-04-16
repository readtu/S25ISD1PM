"""URL configuration for chairs_project project."""

from django.contrib.staticfiles.urls import urlpatterns
from django.urls import include, path

urlpatterns = [
    path("", include("chairs_app.urls")),
    path("", include("locations_app.urls")),
    path("", include("changes_app.urls")),
    path("", include("semesters_app.urls")),
    path("", include("help_app.urls")),
    path("", include("departments_app.urls")),
    *urlpatterns,
]
