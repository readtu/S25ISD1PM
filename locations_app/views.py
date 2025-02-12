from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST


@require_GET
def list_buildings(request: HttpRequest) -> HttpResponse:
    return render(request, "locations_app/list_buildings.html", {})


@require_http_methods(["GET", "POST"])
def create_building(request: HttpRequest) -> HttpResponse:
    return render(request, "locations_app/create_building.html", {})


@require_GET
def view_building(request: HttpRequest, uuid: str) -> HttpResponse:
    return render(request, "locations_app/view_building.html", {})


@require_http_methods(["GET", "POST"])
def edit_building(request: HttpRequest, uuid: str) -> HttpResponse:
    return render(request, "locations_app/edit_building.html", {})


@require_POST
def delete_building(request: HttpRequest, uuid: str) -> HttpResponse:
    return redirect(list_buildings.__name__)


@require_GET
def list_rooms(request: HttpRequest) -> HttpResponse:
    return render(request, "locations_app/list_rooms.html", {})


@require_http_methods(["GET", "POST"])
def create_room(request: HttpRequest) -> HttpResponse:
    return render(request, "locations_app/create_room.html", {})


@require_GET
def view_room(request: HttpRequest, uuid: str) -> HttpResponse:
    return render(request, "locations_app/view_room.html", {})


@require_http_methods(["GET", "POST"])
def edit_room(request: HttpRequest, uuid: str) -> HttpResponse:
    return render(request, "locations_app/edit_room.html", {})


@require_POST
def delete_room(request: HttpRequest, uuid: str) -> HttpResponse:
    return redirect(list_rooms.__name__)
