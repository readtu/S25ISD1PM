from django.urls.conf import path

from . import views

urlpatterns = [
    path(
        "departments",
        views.list_departments,
        name=views.list_departments.__name__,
    ),
    path(
        "departments/create",
        views.create_department,
        name=views.create_department.__name__,
    ),
    path(
        "departments/<uuid:uuid>/edit",
        views.edit_department,
        name=views.edit_department.__name__,
    ),
    path(
        "departments/<uuid:uuid>/delete",
        views.delete_department,
        name=views.delete_department.__name__,
    ),
    path(
        "schools/create",
        views.create_school,
        name=views.create_school.__name__,
    ),
    path(
        "schools/<uuid:uuid>/edit",
        views.edit_school,
        name=views.edit_school.__name__,
    ),
    path(
        "schools/<uuid:uuid>/delete",
        views.delete_school,
        name=views.delete_school.__name__,
    ),
    path(
        "subject/create",
        views.create_subject,
        name=views.create_subject.__name__,
    ),
    path(
        "subject/<uuid:uuid>/edit",
        views.edit_subject,
        name=views.edit_subject.__name__,
    ),
    path(
        "subject/<uuid:uuid>/delete",
        views.delete_subject,
        name=views.delete_subject.__name__,
    ),
]
