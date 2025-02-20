from django.urls.conf import path

from semesters_app import views

urlpatterns = [
    path(
        "semesters",
        views.list_semesters,
        name=views.list_semesters.__name__,
    ),
    path(
        "semesters/create",
        views.create_semester,
        name=views.create_semester.__name__,
    ),
    path(
        "semesters/<uuid:uuid>",
        views.view_semester,
        name=views.view_semester.__name__,
    ),
    path(
        "semesters/<uuid:uuid>/copy_to",
        views.copy_to_semester,
        name=views.copy_to_semester.__name__,
    ),
]
