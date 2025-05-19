from uuid import uuid4

from django.db.models import Model
from django.db.models.deletion import SET_NULL
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField, DateTimeField, UUIDField
from django.db.models.fields.json import JSONField
from django.db.models.fields.related import ForeignKey

from courses_app.models import Section


class ChangeStatus(TextChoices):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ChangeType(TextChoices):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class Change(Model):
    uuid = UUIDField(primary_key=True, default=uuid4)
    date = DateTimeField(auto_now_add=True)
    status = CharField(max_length=10, choices=ChangeStatus.choices, blank=True, default="pending")
    type = CharField(max_length=10, choices=ChangeType.choices)
    data = JSONField(null=True, blank=True)
    section = ForeignKey(
        Section,
        on_delete=SET_NULL,
        related_name="changes",
        null=True,
    )

    def __str__(self):
        return f"{self.get_status_display()} request to {self.get_type_display().lower()} {self.section}"
