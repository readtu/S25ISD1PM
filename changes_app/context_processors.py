from typing import Any

from django.http import HttpRequest


def changes_context_processor(request: HttpRequest) -> dict[str, Any]:
    return {
        "all_changes": [],
        "recent_changes": [],
        "pending_changes": [],
        "accepted_changes": [],
        "rejected_changes": [],
    }
