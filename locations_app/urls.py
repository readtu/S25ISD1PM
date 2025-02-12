from django.urls.conf import path

from locations_app import views

urlpatterns = [
    path(
        "buildings",
        views.list_buildings,
        name=views.list_buildings.__name__,
    ),
    path(
        "buildings/create",
        views.create_building,
        name=views.create_building.__name__,
    ),
    path(
        "buildings/<uuid:uuid>",
        views.view_building,
        name=views.view_building.__name__,
    ),
    path(
        "buildings/<uuid:uuid>/edit",
        views.edit_building,
        name=views.edit_building.__name__,
    ),
    path(
        "buildings/<uuid:uuid>/delete",
        views.delete_building,
        name=views.delete_building.__name__,
    ),
    path(
        "rooms",
        views.list_rooms,
        name=views.list_rooms.__name__,
    ),
    path(
        "rooms/create",
        views.create_room,
        name=views.create_room.__name__,
    ),
    path(
        "rooms/<uuid:uuid>",
        views.view_room,
        name=views.view_room.__name__,
    ),
    path(
        "rooms/<uuid:uuid>/edit",
        views.edit_room,
        name=views.edit_room.__name__,
    ),
    path(
        "rooms/<uuid:uuid>/delete",
        views.delete_room,
        name=views.delete_room.__name__,
    ),
]
