# ruff: noqa: D105

from uuid import uuid4

from django.db.models import Model
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import BooleanField, CharField, UUIDField
from django.db.models.fields.related import ForeignKey

from departments_app.models import Subject
from locations_app.models import Room
from semesters_app.models import Semester


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
    semester = ForeignKey(Semester, on_delete=CASCADE, related_name="sections")
    room = ForeignKey(Room, on_delete=SET_NULL, related_name="sections", null=True)
    is_suggestion = BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.course.name}, offered in {self.semester}"
