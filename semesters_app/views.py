from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.views.decorators.http import require_GET, require_http_methods

from semesters_app.models import (
    AcademicYear,
    Semester,
    group_semesters_by_academic_year,
    group_semesters_by_year,
)


@require_GET
def list_semesters(request: HttpRequest) -> HttpResponse:
    group_by_academic_year: bool = (
        request.GET.get("group_by", "academic_year") == "academic_year"
    )
    semesters = Semester.objects.all().order_by("year", "term").reverse()
    if group_by_academic_year:
        years = group_semesters_by_academic_year(semesters)
    else:
        years = group_semesters_by_year(semesters)
    now_academic_year = AcademicYear(now().year)
    years.setdefault(now_academic_year, [])
    return render(
        request,
        "semesters_app/list_semesters.html",
        {
            "semesters": semesters,
            "years": years.items(),
            "now_academic_year": now_academic_year,
            "group_by_academic_year": group_by_academic_year,
        },
    )


@require_http_methods(["GET", "POST"])
def create_semester(request: HttpRequest) -> HttpResponse:
    return render(request, "semesters_app/create_semester.html", {})


@require_http_methods(["GET", "POST"])
def edit_semester(request: HttpRequest, uuid: str) -> HttpResponse:
    return render(request, "semesters_app/edit_semester.html", {})


@require_http_methods(["GET", "POST"])
def copy_to_semester(request: HttpRequest, uuid: str) -> HttpResponse:
    return render(request, "semesters_app/copy_to_semester.html", {})
