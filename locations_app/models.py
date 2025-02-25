# ruff: noqa: D105

from uuid import uuid4

from django.db.models import Model
from django.db.models.deletion import SET_NULL
from django.db.models.fields import BooleanField, CharField, UUIDField
from django.db.models.fields.related import ForeignKey
from django.urls import reverse


class Building(Model):  # noqa: D101
    uuid = UUIDField(primary_key=True, default=uuid4)
    identifier = CharField(max_length=10, unique=True)
    name = CharField(max_length=255, unique=True)
    available = BooleanField(default=True)

    class Meta:  # noqa: D106
        ordering = ("name",)

    def __str__(self) -> str:
        return f"{self.name} ({self.identifier})"

    def get_absolute_url(self) -> str:  # noqa: D102
        return reverse("view_building", kwargs={"uuid": self.uuid})


class Room(Model):  # noqa: D101
    uuid = UUIDField(primary_key=True, default=uuid4)
    building = ForeignKey(Building, on_delete=SET_NULL, related_name="rooms", null=True)
    name = CharField(max_length=255, null=True, unique=True)
    code = CharField(max_length=10, null=True)
    available = BooleanField(default=True)

    class Meta:  # noqa: D106
        ordering = ("building", "code", "name")

    def __str__(self) -> str:
        s = ""
        if self.code and self.building:
            s = f"{self.building.identifier} {self.code}".strip()
        if self.name:
            s = f"{s} ({self.name})" if s else self.name
        return s

    def get_absolute_url(self) -> str:  # noqa: D102
        return reverse("view_room", kwargs={"uuid": self.uuid})
