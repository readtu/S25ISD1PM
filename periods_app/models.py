# ruff: noqa: D105

from enum import auto
from uuid import uuid4

from django.db.models import SET_NULL, Model
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField, DateField, UUIDField
from django.db.models.fields.related import ForeignKey
from django.urls import reverse


class PeriodTypes(TextChoices):
    YEAR = "year"
    TERM = "term"
    SUBTERM = "subterm"


class TermNames(TextChoices):
    FALL = auto()
    SPRING = auto()
    SUMMER = auto()
    WINTER = auto()
    INTERTERM = auto()
    TUO = auto()


class Period(Model):
    uuid = UUIDField(primary_key=True, default=uuid4)
    title = CharField(max_length=100)
    start = DateField()
    end = DateField()

    type = CharField(choices=PeriodTypes.choices, max_length=50)

    parent = ForeignKey(
        "self",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="sub_periods",
    )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        assert self.type == PeriodTypes.SUBTERM
        return reverse("view_subterm", kwargs={"uuid": self.uuid})
