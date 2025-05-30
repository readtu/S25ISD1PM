# ruff: noqa: D103

from django.contrib.messages import success
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from changes_app.models import Change, ChangeStatus


@require_GET
def list_changes(request: HttpRequest) -> HttpResponse:
    group_by_period = request.GET.get("group_by", "none") == "period"
    status = request.GET.get("status", "any")
    changes = Change.objects.all()
    if status in ChangeStatus:
        changes = changes.filter(status=status)
    return render(
        request,
        f"{__package__}/{list_changes.__name__}.html",
        {
            "group_by_period": group_by_period,
            "status": status,
            "changes": changes,
        },
    )


@require_POST
def accept_change(request: HttpRequest, uuid: str) -> HttpResponse:
    change = get_object_or_404(Change, uuid=uuid)
    # TODO: accept the change
    string = str(change)
    change.status = ChangeStatus.ACCEPTED
    change.save()
    success(request, f"Accepted {string}.")
    return redirect("list_changes")


@require_POST
def reject_change(request: HttpRequest, uuid: str) -> HttpResponse:
    change = get_object_or_404(Change, uuid=uuid)
    # TODO: reject the change
    string = str(change)
    change.status = ChangeStatus.REJECTED
    change.save()
    success(request, f"Rejected {string}.")
    return redirect("list_changes")
