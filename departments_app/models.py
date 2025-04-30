# ruff: noqa: D101, D102, D105, D106

from uuid import uuid4

from django.db.models import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, UUIDField
from django.db.models.fields.related import ForeignKey


class School(Model):
    uuid = UUIDField(primary_key=True, default=uuid4)
    name = CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Department(Model):
    uuid = UUIDField(primary_key=True, default=uuid4)
    name = CharField(max_length=255)
    school = ForeignKey(School, on_delete=CASCADE, related_name="departments")

    def __str__(self) -> str:
        return self.name


class Subject(Model):
    uuid = UUIDField(primary_key=True, default=uuid4)
    code = CharField(max_length=255)
    name = CharField(max_length=255)
    department = ForeignKey(Department, on_delete=CASCADE, related_name="subjects", null=True)

    class Meta:
        ordering = ["code"]

    def __str__(self) -> str:
        return self.code
