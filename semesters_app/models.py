# ruff: noqa: D105

from collections.abc import Iterable
from uuid import uuid4

from django.db.models import Model
from django.db.models.enums import IntegerChoices
from django.db.models.fields import IntegerField, UUIDField
from django.urls import reverse


class Term(IntegerChoices):
    """Represents which term of the year a semester takes place.

    These are enumerated in order they appear on the calendar,
    so they can be used to sort a sequence of Semesters in chronological order."""

    INTERTERM = 1, "Interterm"
    SPRING = 2, "Spring"
    SUMMER = 3, "Summer"
    FALL = 4, "Fall"


class AcademicYear(int):
    """Represents an academic year, like 2024-2025.

    Is and behaves like a normal `int` except the modifications made below."""

    def __contains__(self, value: "Semester | AcademicYear") -> bool:
        """Determine if a given semester is within this academic year.

        For example, Interterm 2024 is `in` the 2024-2025 academic year."""
        if isinstance(value, Semester):
            return value.academic_year == self
        return value == self or value - 1 == self

    def __str__(self) -> str:
        """Return a hyphenated representation of this academic year.

        For example, `AcademicYear(2024)` prints out as `2024-2025`."""
        return f"{type(super()).__str__(self)}-{type(super()).__str__(self + 1)}"


class Semester(Model):  # noqa: D101
    uuid = UUIDField(primary_key=True, default=uuid4)
    year = IntegerField()
    term = IntegerField(choices=Term.choices)

    class Meta:  # noqa: D106
        ordering = ("-year", "-term")
        get_latest_by = ordering
        unique_together = ("year", "term")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:  # noqa: D102
        return reverse("view_semester", kwargs={"uuid": self.uuid})

    @property
    def academic_year(self) -> AcademicYear:
        return AcademicYear(self.year - (self.term != Term.FALL))

    @property
    def name(self) -> str:
        return f"{self.get_term_display()} {self.year}"  # type: ignore[attr-defined]


def group_semesters_by_year(
    semesters: Iterable[Semester],
) -> dict[int, list[Semester]]:
    years = {}
    for semester in semesters:
        years.setdefault(semester.year, []).append(semester)
    return years


def group_semesters_by_academic_year(
    semesters: Iterable[Semester],
) -> dict[AcademicYear, list[Semester]]:
    years = {}
    for semester in semesters:
        years.setdefault(semester.academic_year, []).append(semester)
    return years
