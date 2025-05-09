# ruff: noqa: D103

from datetime import datetime, timedelta

from django.contrib.messages import success
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from courses_app.models import Section
from semesters_app.models import (
    AcademicYear,
    Semester,
    Term,
    group_semesters_by_academic_year,
    group_semesters_by_year,
)
from users_app.models import User, UserRole


@require_GET
def list_semesters(request: HttpRequest) -> HttpResponse:
    group_by_academic_year: bool = request.GET.get("group_by", "academic_year") == "academic_year"
    semesters = Semester.objects.all()
    if group_by_academic_year:
        years = group_semesters_by_academic_year(semesters)
    else:
        years = group_semesters_by_year(semesters)
    now_academic_year = AcademicYear(now().year)
    years.setdefault(now_academic_year, [])
    return render(
        request,
        f"{__package__}/{list_semesters.__name__}.html",
        {
            "semesters": semesters,
            "years": years.items(),
            "now_academic_year": now_academic_year,
            "group_by_academic_year": group_by_academic_year,
        },
    )


@require_http_methods(["GET", "POST"])
def create_semester(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        semester = Semester.objects.create(
            year=request.POST["year"],
            term=Term(int(request.POST["term"])),
        )
        success(request, f"Created {semester}.")
        return redirect(semester)
    now_ = now().year
    return render(
        request,
        f"{__package__}/{create_semester.__name__}.html",
        {
            "now": now_,
        },
    )


@require_http_methods(["GET", "POST"])
def view_semester(request: HttpRequest, uuid: str) -> HttpResponse:
    semester = get_object_or_404(Semester, uuid=uuid)
    sections = Section.objects.filter(semester=semester)
    course_codes = sorted({section.course.code for section in sections})
    professors = User.objects.filter(role=UserRole.PROFESSOR).order_by("name")
    subjects = {section.course.subject for section in sections}
    rooms = {section.room for section in sections}
    events = []
    for section in sections:
        semester_offset = semester.start
        while semester_offset <= semester.end:
            if str(semester_offset.weekday()) in section.days_of_week:
                events.append(
                    {
                        "title": section.course.code,
                        "start": datetime.combine(semester_offset, section.start_time),
                        "end": datetime.combine(semester_offset, section.end_time),
                    },
                )
            semester_offset += timedelta(days=1)

    return render(
        request,
        f"{__package__}/{view_semester.__name__}.html",
        {
            "semester": semester,
            "sections": sections,
            "course_codes": course_codes,
            "professors": professors,
            "rooms": rooms,
            "subjects": subjects,
            "events": events,
        },
    )


@require_http_methods(["GET", "POST"])
def copy_to_semester(request: HttpRequest, uuid: str) -> HttpResponse:
    semester = get_object_or_404(Semester, uuid=uuid)
    years = group_semesters_by_year(Semester.objects.all().exclude(uuid=semester.uuid))
    if request.method == "POST":
        from_ = get_object_or_404(Semester, uuid=request.POST["from"])
        # TODO: copy the information from one semester to the other
        success(request, f"Copied from {from_} to {semester}.")
        return redirect(semester)
    return render(
        request,
        f"{__package__}/{copy_to_semester.__name__}.html",
        {
            "semester": semester,
            "years": years,
        },
    )


@require_POST
def delete_semester(request: HttpRequest, uuid: str) -> HttpResponse:
    semester = get_object_or_404(Semester, uuid=uuid)
    name = str(semester)
    semester.delete()
    success(request, f"Deleted {name}.")
    return redirect(list_semesters.__name__)
