# ruff: noqa: D101, D105, D106

from uuid import uuid4

from django.db.models import F, Model, Q
from django.db.models.constraints import CheckConstraint
from django.db.models.deletion import SET_NULL
from django.db.models.fields import BooleanField, CharField, PositiveIntegerField, UUIDField
from django.db.models.fields.related import ForeignKey
from django.urls import reverse


class Building(Model):
    uuid = UUIDField(primary_key=True, default=uuid4)
    code = CharField(max_length=10)
    name = CharField(max_length=255)
    available = BooleanField(default=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"

    def get_absolute_url(self) -> str:  # noqa: D102
        return reverse("view_building", kwargs={"uuid": self.uuid})


class Room(Model):
    uuid = UUIDField(primary_key=True, default=uuid4)
    building = ForeignKey(Building, on_delete=SET_NULL, related_name="rooms", null=True)
    name = CharField(max_length=255, null=True)
    code = CharField(max_length=10, null=True)
    available = BooleanField(default=True)
    default_capacity = PositiveIntegerField()
    maximum_capacity = PositiveIntegerField()

    class Meta:
        ordering = ("building", "code", "name")
        constraints = (
            CheckConstraint(
                check=Q(maximum_capacity__gte=F("default_capacity")),
                name="maximum_capacity_must_be_greater_than_default_capacity",
                violation_error_message=(
                    "The maximum_capacity of a Room must be "
                    "greater than or equal to its default_capacity."
                ),
            ),
        )

    def __str__(self) -> str:
        s = ""
        if self.code and self.building:
            s = f"{self.building.code} {self.code}".strip()
        if self.name:
            s = f"{s} ({self.name})" if s else self.name
        return s

    def get_absolute_url(self) -> str:  # noqa: D102
        return reverse("view_room", kwargs={"uuid": self.uuid})
