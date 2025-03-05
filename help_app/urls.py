from django.urls.conf import path

from . import views

urlpatterns = [
    path(
        "help",
        views.list_articles,
        name=views.list_articles.__name__,
    ),
    path(
        "help/create",
        views.create_article,
        name=views.create_article.__name__,
    ),
    path(
        "help/<slug:slug>",
        views.view_article,
        name=views.view_article.__name__,
    ),
    path(
        "help/<slug:slug>/edit",
        views.edit_article,
        name=views.edit_article.__name__,
    ),
    path(
        "help/<slug:slug>/delete",
        views.delete_article,
        name=views.delete_article.__name__,
    ),
]
