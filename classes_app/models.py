from uuid import uuid4

from django.db.models import Model
from django.db.models.deletion import SET_NULL
from django.db.models.fields import CharField, UUIDField
from django.db.models.fields.related import ForeignKey


class Department(Model):
    uuid = UUIDField(primary_key=True, default=uuid4)
    name = CharField(max_length=255)
    identifier = CharField(max_length=10, unique=True)


class Class(Model):
    uuid = UUIDField(primary_key=True, default=uuid4)
    name = CharField(max_length=255)
    department = ForeignKey(Department, on_delete=SET_NULL, related_name="classes", null=True)
    code = CharField(max_length=10)

    def __str__(self) -> str:
        return self.name
