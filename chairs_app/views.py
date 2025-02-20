from django.shortcuts import render
from django.views.decorators.http import require_safe


@require_safe
def home(request):
    return render(request, f"chairs_app/{home.__name__}.html")
