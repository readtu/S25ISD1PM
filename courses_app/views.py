from typing import Any

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from courses_app.models import Course


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
        k: {kk: vv for kk, vv in sorted(v.items(), key=lambda i: i[0])}
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
