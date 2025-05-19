# ruff: noqa: D103

from datetime import date, datetime, timedelta
from http import HTTPMethod

from django.contrib.messages import success
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from changes_app.models import Change, ChangeStatus, ChangeType
from courses_app.models import Section
from periods_app.models import Period, PeriodTypes, TermNames
from users_app.models import User, UserRole


@require_GET
def list_periods(request: HttpRequest) -> HttpResponse:
    years = {
        year: {
            term: term.sub_periods.order_by("-start", "end")
            for term in year.sub_periods.order_by("-start", "end")
        }
        for year in Period.objects.filter(type=PeriodTypes.YEAR).order_by("-start", "end")
    }
    return render(
        request,
        f"{__package__}/{list_periods.__name__}.html",
        {
            "years": years,
        },
    )


@require_http_methods([HTTPMethod.GET, HTTPMethod.POST])
def create_year(request: HttpRequest) -> HttpResponse:
    if request.method == HTTPMethod.POST:
        start = date.fromisoformat(request.POST["start"])
        end = date.fromisoformat(request.POST["end"])
        title = f"{f'{start.year}-{end.year}' if start.year != end.year else f'{start.year}'} Academic Year"
        year = Period.objects.create(
            type=PeriodTypes.YEAR,
            title=title,
            start=start,
            end=end,
        )
        success(request, f"Created {year}.")
        return redirect("list_periods")
    return render(request, f"{__package__}/{create_year.__name__}.html")


@require_http_methods([HTTPMethod.GET, HTTPMethod.POST])
def create_term(request: HttpRequest, year_uuid: str) -> HttpResponse:
    year = get_object_or_404(
        Period.objects.filter(type=PeriodTypes.YEAR),
        uuid=year_uuid,
    )
    if request.method == HTTPMethod.POST:
        start = date.fromisoformat(request.POST["start"])
        end = date.fromisoformat(request.POST["end"])
        term_name = request.POST["term_name"]
        title = f"{term_name.title()} {start.year}"
        term = Period.objects.create(
            type=PeriodTypes.TERM,
            title=title,
            start=start,
            end=end,
            parent=year,
        )
        success(request, f"Created {term}.")
        return redirect("list_periods")
    return render(
        request,
        f"{__package__}/{create_term.__name__}.html",
        {
            "year": year,
            "term_names": TermNames,
        },
    )


@require_http_methods([HTTPMethod.GET, HTTPMethod.POST])
def create_subterm(
    request: HttpRequest,
    year_uuid: str,
    term_uuid: str,
) -> HttpResponse:
    year = get_object_or_404(
        Period.objects.filter(type=PeriodTypes.YEAR),
        uuid=year_uuid,
    )
    term = get_object_or_404(
        year.sub_periods.filter(type=PeriodTypes.TERM),
        uuid=term_uuid,
    )
    if request.method == HTTPMethod.POST:
        start = date.fromisoformat(request.POST["start"])
        end = date.fromisoformat(request.POST["end"])
        title = request.POST["title"]
        subterm = Period.objects.create(
            type=PeriodTypes.SUBTERM,
            title=title,
            start=start,
            end=end,
            parent=term,
        )
        success(request, f"Created {subterm}.")
        return redirect(subterm)
    return render(
        request,
        f"{__package__}/{create_subterm.__name__}.html",
        {
            "year": year,
            "term": term,
        },
    )


@require_http_methods([HTTPMethod.GET, HTTPMethod.POST])
def view_subterm(request: HttpRequest, uuid: str) -> HttpResponse:
    period = get_object_or_404(Period, uuid=uuid)
    sections = (
        Section.objects.filter(period=period)
        .select_related("course", "course__subject")
        .order_by("course__subject__code", "course__number", "start_time")
    )
    course_codes = sorted({section.course.code for section in sections})
    professors = User.objects.filter(role=UserRole.PROFESSOR).order_by("name")
    subjects = sorted(
        {section.course.subject for section in sections},
        key=lambda subject: (subject.code,),
    )
    rooms = sorted(
        {section.room for section in sections},
        key=lambda room: (
            room.building.code,
            room.code,
        ),
    )
    events = []
    for section in sections:
        period_offset = period.start
        while period_offset <= period.end:
            if str(period_offset.weekday()) in section.days_of_week:
                events.append(
                    {
                        "title": section.course.code,
                        "start": datetime.combine(period_offset, section.start_time),
                        "end": datetime.combine(period_offset, section.end_time),
                    },
                )
            period_offset += timedelta(days=1)

    return render(
        request,
        f"{__package__}/{view_subterm.__name__}.html",
        {
            "period": period,
            "sections": sections,
            "course_codes": course_codes,
            "professors": professors,
            "rooms": rooms,
            "subjects": subjects,
            "events": events,
        },
    )


@require_POST
def delete_period(request: HttpRequest, uuid: str) -> HttpResponse:
    period = get_object_or_404(Period, uuid=uuid)
    name = str(period)
    period.delete()
    success(request, f"Deleted {name}.")
    return redirect(list_periods.__name__)


@require_POST
def create_changes(request: HttpRequest, uuid: str) -> HttpResponse:
    period = get_object_or_404(Period, uuid=uuid)
    for section in period.sections.all():
        if section.is_suggestion:
            continue
        if section.changes.exclude(status=ChangeStatus.REJECTED).exists():
            continue
        Change.objects.create(
            section=section,
            type=ChangeType.CREATE,
            status=ChangeStatus.PENDING,
        )
    success(request, f"Created changes for {period}.")
    return redirect("list_changes")
