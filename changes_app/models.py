from django.db.models import Model
from django.db.models.deletion import SET_NULL
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField, UUIDField
from django.db.models.fields.related import ForeignKey

from periods_app.models import Period


class ChangeStatus(TextChoices):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Change(Model):
    uuid = UUIDField(primary_key=True)
    status = CharField(max_length=10, choices=ChangeStatus.choices, blank=True, default="pending")
    period = ForeignKey(
        Period,
        on_delete=SET_NULL,
        related_name="changes",
        null=True,
    )
