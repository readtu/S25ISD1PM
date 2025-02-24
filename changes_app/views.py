# ruff: noqa: D103

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST


@require_GET
def list_changes(request: HttpRequest) -> HttpResponse:
    return render(request, f"changes_app/{list_changes.__name__}.html", {})


@require_POST
def accept_change(request: HttpRequest, uuid: str) -> HttpResponse: ...


@require_POST
def reject_change(request: HttpRequest, uuid: str) -> HttpResponse: ...
