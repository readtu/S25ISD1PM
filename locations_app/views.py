# ruff: noqa: D103

from http import HTTPMethod

from django.contrib.messages import success
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from locations_app.models import Building, Room


@require_GET
def list_buildings(request: HttpRequest) -> HttpResponse:
    buildings = Building.objects.all()
    return render(
        request,
        f"{__package__}/{list_buildings.__name__}.html",
        {
            "buildings": buildings,
        },
    )


@require_http_methods([HTTPMethod.GET, HTTPMethod.POST])
def create_building(request: HttpRequest) -> HttpResponse:
    if request.method == HTTPMethod.POST:
        building = Building.objects.create(
            identifier=request.POST["identifier"],
            name=request.POST["name"],
        )
        success(request, f"Created {building}.")
        return redirect(building)
    return render(request, f"{__package__}/{create_building.__name__}.html", {})


@require_GET
def view_building(request: HttpRequest, uuid: str) -> HttpResponse:
    building = get_object_or_404(Building, uuid=uuid)
    return render(
        request,
        f"{__package__}/{view_building.__name__}.html",
        {
            "building": building,
            "classes": building.classes.all(),
        },
    )


@require_http_methods([HTTPMethod.GET, HTTPMethod.POST])
def edit_building(request: HttpRequest, uuid: str) -> HttpResponse:
    building = get_object_or_404(Building, uuid=uuid)
    if request.method == HTTPMethod.POST:
        building.name = request.POST["name"]
        building.code = request.POST["identifier"]
        building.available = request.POST.get("available", "off") == "on"
        building.save()
        success(request, f"Saved changes to {building.name}.")
        return redirect(building)
    return render(
        request,
        f"{__package__}/{edit_building.__name__}.html",
        {
            "building": building,
        },
    )


@require_POST
def toggle_building_availability(request: HttpRequest, uuid: str) -> HttpResponse:
    building = get_object_or_404(Building, uuid=uuid)
    building.available = not building.available
    building.save()
    success(request, f"Made {building} {'available' if building.available else 'unavailable'}.")
    return redirect(building)


@require_POST
def delete_building(request: HttpRequest, uuid: str) -> HttpResponse:
    building = get_object_or_404(Building, uuid=uuid)
    name = str(building)
    building.delete()
    success(request, f"Deleted {name}.")
    return redirect(list_buildings.__name__)


@require_GET
def list_rooms(request: HttpRequest) -> HttpResponse:
    rooms = Room.objects.all()
    group_by_building = request.GET.get("group_by", "building") == "building"
    availability = request.GET.get("availability", "all") == "available"
    sort_by = request.GET.get("sort_by", "identifier")
    if sort_by in {"default_capacity", "maximum_capacity"}:
        rooms = rooms.order_by(sort_by).reverse()
    if availability:
        rooms = rooms.filter(available=True, building__available=True)
    groups = {}
    for room in rooms:
        groups.setdefault(room.building, []).append(room)
    return render(
        request,
        f"{__package__}/{list_rooms.__name__}.html",
        {
            "rooms": rooms,
            "groups": groups,
            "group_by_building": group_by_building,
            "availability": availability,
            "sort_by": sort_by,
        },
    )


@require_http_methods([HTTPMethod.GET, HTTPMethod.POST])
def create_room(request: HttpRequest, building_uuid: str) -> HttpResponse:
    building = get_object_or_404(Building, uuid=building_uuid)
    if request.method == HTTPMethod.POST:
        room = Room.objects.create(
            building=building,
            name=request.POST.get("name", "") or None,
            number=request.POST.get("code", "") or None,
            default_capacity=int(request.POST["default_capacity"]),
            maximum_capacity=int(request.POST["maximum_capacity"]),
        )
        success(request, f"Created {room}.")
        return redirect(room)
    return render(
        request,
        f"{__package__}/{create_room.__name__}.html",
        {
            "building": building,
        },
    )


@require_GET
def view_room(request: HttpRequest, uuid: str) -> HttpResponse:
    room = get_object_or_404(Room, uuid=uuid)
    return render(
        request,
        f"{__package__}/{view_room.__name__}.html",
        {
            "room": room,
        },
    )


@require_http_methods([HTTPMethod.GET, HTTPMethod.POST])
def edit_room(request: HttpRequest, uuid: str) -> HttpResponse:
    room = get_object_or_404(Room, uuid=uuid)
    if request.method == HTTPMethod.POST:
        room.name = request.POST.get("name", "") or None
        room.number = request.POST.get("code", "") or None
        room.available = request.POST.get("available", "off") == "on"
        room.default_capacity = int(request.POST["default_capacity"])
        room.maximum_capacity = int(request.POST["maximum_capacity"])
        room.save()
        success(request, f"Saved changes to {room}.")
        return redirect(room)
    return render(
        request,
        f"{__package__}/{edit_room.__name__}.html",
        {
            "room": room,
        },
    )


@require_POST
def toggle_room_availability(request: HttpRequest, uuid: str) -> HttpResponse:
    room = get_object_or_404(Room, uuid=uuid)
    room.available = not room.available
    room.save()
    success(request, f"Made {room} {'available' if room.available else 'unavailable'}.")
    return redirect(room)


@require_POST
def delete_room(request: HttpRequest, uuid: str) -> HttpResponse:
    room = get_object_or_404(Room, uuid=uuid)
    name = str(room)
    room.delete()
    success(request, f"Deleted {name}.")
    return redirect(list_rooms.__name__)
