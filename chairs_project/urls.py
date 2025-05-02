"""URL configuration for chairs_project project."""

from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.contrib.staticfiles.urls import urlpatterns as static_urlpatterns
from django.urls.conf import include, path

urlpatterns = []

for app_config in apps.get_app_configs():
    urls_path = Path(app_config.path)
    if not urls_path.is_relative_to(settings.BASE_DIR):
        continue
    if not (Path(urls_path) / "urls.py").exists():
        continue
    urlpatterns.append(
        path("", include(f"{urls_path.name}.urls")),
    )

urlpatterns.extend(static_urlpatterns)
