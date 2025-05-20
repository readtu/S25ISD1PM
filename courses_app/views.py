import time
from http import HTTPMethod
from typing import Any

from django.contrib.messages import success, warning
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from chairs_project.rules import RULES
from chairs_project.utils import DAYS_OF_WEEK_NAME
from courses_app.models import Course, Section
from departments_app.models import Subject
from locations_app.models import Building, Room
from periods_app.models import Period, PeriodTypes


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
    subjects = dict(
        filter(
            lambda item: item[1],
            {
                subject: dict(
                    sorted(
                        {
                            (course.code, course.name): course for course in subject.courses.all()
                        }.items(),
                    ),
                )
                for subject in Subject.objects.all()
            }.items(),
        ),
    )
    years = {
        year: [
            (term, subterm)
            for term in year.sub_periods.all().order_by("-start")
            for subterm in term.sub_periods.all().order_by("-start")
        ]
        for year in Period.objects.filter(type=PeriodTypes.YEAR).order_by("-start")
    }
    if request.method == HTTPMethod.POST:
        period = Period.objects.get(uuid=request.POST["period"])
        course = Course.objects.get(uuid=request.POST["course"])
        room = Room.objects.get(uuid=request.POST["room"])
        days_of_week = "".join(key[-1] for key in request.POST if key.startswith("day_of_week_"))
        section = Section(
            period=period,
            course=course,
            room=room,
            capacity=request.POST["capacity"],
            start_time=request.POST["start_time"],
            end_time=request.POST["end_time"],
            days_of_week=days_of_week,
            is_suggestion=False,
        )

        # Perform audits
        section.full_clean()
        for Rule in RULES:
            try:
                Rule.check_section(section)
            except AssertionError as e:
                warning(request, str(e) + "")
                break
        else:
            section.save()
            success(request, f"Created {section}.")
            return redirect(period)

    return render(
        request,
        f"{__package__}/{create_section.__name__}.html",
        {
            "buildings": Building.objects.all(),
            "subjects": subjects,
            "years": years,
            "days_of_week": enumerate(DAYS_OF_WEEK_NAME),
        },
    )


@require_http_methods([HTTPMethod.GET, HTTPMethod.POST])
def edit_section(request: HttpRequest, uuid: str) -> HttpResponse:
    section = Section.objects.get(uuid=uuid)
    if request.method == HTTPMethod.POST:
        section.capacity = int(request.POST["capacity"])
        section.start_time = request.POST["start_time"]
        section.end_time = request.POST["end_time"]

        # Perform audits
        section.full_clean()
        for Rule in RULES:
            try:
                Rule.check_section(section)
            except AssertionError as e:
                warning(request, str(e) + "")
                break
        else:
            section.save()
            success(request, f"Saved changes to {success}.")
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
