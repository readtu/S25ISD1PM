from django.contrib.messages import success
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from locations_app.models import Building


@require_GET
def list_buildings(request: HttpRequest) -> HttpResponse:
    buildings = Building.objects.all().order_by("identifier")
    return render(
        request,
        f"locations_app/{list_buildings.__name__}.html",
        {
            "buildings": buildings,
        },
    )


@require_http_methods(["GET", "POST"])
def create_building(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        building = Building.objects.create(
            identifier=request.POST["identifier"],
            name=request.POST["name"],
        )
        success(request, f"Created {building}.")
        return redirect(building)
    return render(request, f"locations_app/{create_building.__name__}.html", {})


@require_GET
def view_building(request: HttpRequest, uuid: str) -> HttpResponse:
    building = get_object_or_404(Building, uuid=uuid)
    return render(request, f"locations_app/{view_building.__name__}.html", {
        "building": building,
    })


@require_http_methods(["GET", "POST"])
def edit_building(request: HttpRequest, uuid: str) -> HttpResponse:
    building = get_object_or_404(Building, uuid=uuid)
    if request.method == "POST":
        building.name = request.POST["name"]
        building.identifier = request.POST["identifier"]
        building.save()
        success(request, f"Saved changes to {building.name}.")
        return redirect(building)
    return render(request, f"locations_app/{edit_building.__name__}.html", {
        "building": building,
    })


@require_POST
def delete_building(request: HttpRequest, uuid: str) -> HttpResponse:
    building = get_object_or_404(Building, uuid=uuid)
    name = building.name
    building.delete()
    success(request, f"Deleted {name}.")
    return redirect(list_buildings.__name__)


@require_GET
def list_rooms(request: HttpRequest) -> HttpResponse:
    return render(request, f"locations_app/{list_rooms.__name__}.html", {})


@require_http_methods(["GET", "POST"])
def create_room(request: HttpRequest) -> HttpResponse:
    return render(request, f"locations_app/{create_room.__name__}.html", {})


@require_GET
def view_room(request: HttpRequest, uuid: str) -> HttpResponse:
    return render(request, f"locations_app/{view_room.__name__}.html", {})


@require_http_methods(["GET", "POST"])
def edit_room(request: HttpRequest, uuid: str) -> HttpResponse:
    return render(request, f"locations_app/{edit_room.__name__}.html", {})


@require_POST
def delete_room(request: HttpRequest, uuid: str) -> HttpResponse:
    return redirect(list_rooms.__name__)
