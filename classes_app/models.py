from uuid import uuid4

from django.db.models import Model
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import BooleanField, CharField, UUIDField
from django.db.models.fields.related import ForeignKey

from departments_app.models import Subject
from locations_app.models import Room
from semesters_app.models import Semester


class Class(Model):
    uuid = UUIDField(primary_key=True, default=uuid4)
    name = CharField(max_length=255)
    subject = ForeignKey(Subject, on_delete=SET_NULL, related_name="classes", null=True)
    room = ForeignKey(Room, on_delete=SET_NULL, related_name="classes", null=True)
    semester = ForeignKey(Semester, on_delete=CASCADE, related_name="classes")
    code = CharField(max_length=10)
    is_suggestion = BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
