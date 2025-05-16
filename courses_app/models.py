# ruff: noqa: D105

from uuid import uuid4

from django.db.models import Model
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import BooleanField, CharField, IntegerField, TimeField, UUIDField
from django.db.models.fields.related import ForeignKey

from chairs_project.utils import DAYS_OF_WEEK_NAME, DaysOfWeek, format_time
from departments_app.models import Subject
from locations_app.models import Room
from periods_app.models import Period


class Course(Model):
    uuid = UUIDField(primary_key=True, default=uuid4)
    name = CharField(max_length=255)
    subject = ForeignKey(Subject, on_delete=CASCADE, related_name="courses")
    number = CharField(max_length=10)

    class Meta:  # noqa: D106
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"

    @property
    def code(self):
        return f"{self.subject} {self.number}"


class Section(Model):
    uuid = UUIDField(primary_key=True, default=uuid4)
    course = ForeignKey(Course, on_delete=CASCADE, related_name="sections")
    period = ForeignKey(Period, on_delete=CASCADE, related_name="sections")
    room = ForeignKey(Room, on_delete=SET_NULL, related_name="sections", null=True)
    capacity = IntegerField()

    days_of_week = CharField(max_length=7)
    start_time = TimeField()
    end_time = TimeField()

    is_suggestion = BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.course.name}, offered in {self.period}"

    @property
    def time_display(self) -> str:
        days_of_week_display = "".join(
            DaysOfWeek(DAYS_OF_WEEK_NAME[int(d)]).value for d in self.days_of_week
        )
        start_time_display = format_time(self.start_time)
        end_time_display = format_time(self.end_time)
        return f"{start_time_display}-{end_time_display} {days_of_week_display}"
