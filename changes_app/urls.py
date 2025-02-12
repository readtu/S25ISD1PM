from django.urls.conf import path

from changes_app import views

urlpatterns = [
    path(
        "changes",
        views.list_changes,
        name=views.list_changes.__name__,
    ),
    path(
        "changes/<uuid:uuid>/accept",
        views.accept_change,
        name=views.accept_change.__name__,
    ),
    path(
        "changes/<uuid:uuid>/reject",
        views.reject_change,
        name=views.reject_change.__name__,
    ),
]
