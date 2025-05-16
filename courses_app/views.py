from http import HTTPMethod
from typing import Any

from django.contrib.messages import success
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from chairs_project.utils import DAYS_OF_WEEK_NAME
from courses_app.models import Course, Section
from locations_app.models import Building


@require_GET
def list_courses(request: HttpRequest) -> HttpResponse:
    courses = Course.objects.select_related("subject").order_by("name", "subject__code")
    expand = request.GET.get("expand", "False") == "True"
    group_by = request.GET.get("group_by", "none")
    combine_by = request.GET.get("combine_by", "False").title() == "True"
    groups = dict[Any, dict[Any, list[Course]]]()
    if group_by == "letter":
        for course in courses:
            groups.setdefault(course.name[0].upper(), {}).setdefault("", []).append(course)
    elif group_by == "subject":
        for course in courses:
            groups.setdefault(course.subject.name, {}).setdefault("", []).append(course)
    else:
        groups.setdefault("", {}).setdefault("", []).extend(courses)
    for group in groups.values():
        key, value = group.popitem()
        for course in value:
            if combine_by:
                group.setdefault(course.code, []).append(course)
            else:
                group.setdefault((course.code, course.uuid), []).append(course)
    groups = {
        k: dict(sorted(v.items(), key=lambda i: i[0]))
        for k, v in sorted(groups.items(), key=lambda i: i[0])
    }
    return render(
        request,
        f"{__package__}/{list_courses.__name__}.html",
        {
            "expand": expand,
            "combine_by": combine_by,
            "group_by": group_by,
            "groups": groups,
        },
    )


@require_http_methods([HTTPMethod.GET, HTTPMethod.POST])
def create_section(request: HttpRequest) -> HttpResponse:
    if request.method == HTTPMethod.POST:
        section = Section.objects.create(...)
        return redirect(section.period)
    return render(request, f"{__package__}/{create_section.__name__}.html", {})


@require_http_methods([HTTPMethod.GET, HTTPMethod.POST])
def edit_section(request: HttpRequest, uuid: str) -> HttpResponse:
    section = Section.objects.get(uuid=uuid)
    if request.method == HTTPMethod.POST:
        section.capacity = int(request.POST["capacity"])
        section.start_time = request.POST["start_time"]
        section.end_time = request.POST["end_time"]
        success(request, f"Saved changes to {section}.")
        section.save()
        return redirect(section.period)
    return render(
        request,
        f"{__package__}/{edit_section.__name__}.html",
        {
            "section": section,
            "buildings": Building.objects.all(),
            "days_of_week": [(str(i), j) for i, j in enumerate(DAYS_OF_WEEK_NAME)],
        },
    )


@require_POST
def delete_section(request: HttpRequest, uuid: str) -> HttpResponse:
    section = get_object_or_404(Section, uuid=uuid)
    name = str(section)
    period = section.period
    section.delete()
    success(request, f"{name} deleted.")
    return redirect(period)


@require_POST
def apply_section(request: HttpRequest, uuid: str) -> HttpResponse:
    section = get_object_or_404(Section, uuid=uuid)
    section.is_suggestion = False
    section.save()
    success(request, f"{section} applied.")
    return redirect(section.period)
