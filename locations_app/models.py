# ruff: noqa: D105

from uuid import uuid4

from django.db.models import Model
from django.db.models.constraints import CheckConstraint
from django.db.models.deletion import SET_NULL
from django.db.models.fields import BooleanField, CharField, UUIDField
from django.db.models.fields.related import ForeignKey
from django.db.models.query_utils import Q
from django.urls import reverse


class Building(Model):  # noqa: D101
    uuid = UUIDField(primary_key=True, default=uuid4)
    identifier = CharField(max_length=10, unique=True)
    name = CharField(max_length=255, unique=True)
    available = BooleanField(default=True)

    def __str__(self) -> str:
        return self.identifier

    def get_absolute_url(self) -> str:  # noqa: D102
        return reverse("view_building", kwargs={"uuid": self.uuid})


class Room(Model):  # noqa: D101
    uuid = UUIDField(primary_key=True, default=uuid4)
    building = ForeignKey(Building, on_delete=SET_NULL, related_name="rooms", null=True)
    name = CharField(max_length=255, null=True, unique=True)
    code = CharField(max_length=10, null=True)
    available = BooleanField(default=True)

    def __str__(self) -> str:
        s = f"{self.building} {self.code}".strip()
        if self.name:
            return f"{self.name} ({s})"
        return s

    def get_absolute_url(self) -> str:  # noqa: D102
        return reverse("view_room", kwargs={"uuid": self.uuid})
