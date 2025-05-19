from django.urls.conf import path

from courses_app import views

urlpatterns = [
    path(
        "courses",
        views.list_courses,
        name=views.list_courses.__name__,
    ),
    path(
        "sections/create",
        views.create_section,
        name=views.create_section.__name__,
    ),
    path(
        "sections/<uuid:uuid>/edit",
        views.edit_section,
        name=views.edit_section.__name__,
    ),
    path(
        "sections/<uuid:uuid>/delete",
        views.delete_section,
        name=views.delete_section.__name__,
    ),
]
