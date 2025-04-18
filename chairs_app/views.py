# ruff: noqa: D103

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_safe


@require_safe
def home(request: HttpRequest) -> HttpResponse:
    return render(request, f"{__package__}/{home.__name__}.html")
