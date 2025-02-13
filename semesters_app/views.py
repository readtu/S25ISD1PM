from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods


@require_GET
def list_semesters(request: HttpRequest) -> HttpResponse:
    return render(request, "semesters_app/list_semesters.html", {})


@require_http_methods(["GET", "POST"])
def create_semester(request: HttpRequest) -> HttpResponse:
    return render(request, "semesters_app/create_semester.html", {})


@require_http_methods(["GET", "POST"])
def edit_semester(request: HttpRequest, uuid: str) -> HttpResponse:
    return render(request, "semesters_app/edit_semester.html", {})


@require_http_methods(["GET", "POST"])
def copy_to_semester(request: HttpRequest, uuid: str) -> HttpResponse:
    return render(request, "semesters_app/copy_to_semester.html", {})
