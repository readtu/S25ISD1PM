from django.urls.conf import path

from periods_app import views

urlpatterns = [
    path(
        "periods",
        views.list_periods,
        name=views.list_periods.__name__,
    ),
    path(
        "periods/years/create",
        views.create_year,
        name=views.create_year.__name__,
    ),
    path(
        "periods/year/<uuid:year_uuid>/terms/create",
        views.create_term,
        name=views.create_term.__name__,
    ),
    path(
        "periods/year/<uuid:year_uuid>/terms/<uuid:term_uuid>/subterms/create",
        views.create_subterm,
        name=views.create_subterm.__name__,
    ),
    path(
        "periods/<uuid:uuid>",
        views.view_subterm,
        name=views.view_subterm.__name__,
    ),
    path(
        "periods/<uuid:uuid>/create_changes",
        views.create_changes,
        name=views.create_changes.__name__,
    ),
    path(
        "periods/<uuid:uuid>/delete",
        views.delete_period,
        name=views.delete_period.__name__,
    ),
]
