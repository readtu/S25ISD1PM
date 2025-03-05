from django.db.models import Model
from django.db.models.enums import TextChoices
from django.db.models.fields import UUIDField


class ChangeStatus(TextChoices):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Change(Model):
    uuid = UUIDField(primary_key=True)

