from typing import Any

from django.http import HttpRequest

from changes_app.models import Change, ChangeStatus


def changes_context_processor(request: HttpRequest) -> dict[str, Any]:
    changes = Change.objects.all()
    return {
        "all_changes": changes,
        "recent_changes": changes,
        "pending_changes": [c for c in changes if c.status == ChangeStatus.PENDING],
        "accepted_changes": [c for c in changes if c.status == ChangeStatus.ACCEPTED],
        "rejected_changes": [c for c in changes if c.status == ChangeStatus.REJECTED],
    }
