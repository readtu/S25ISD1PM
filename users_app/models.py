from enum import auto
from uuid import uuid4

from django.db.models import Model
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField, EmailField, UUIDField


class UserRole(TextChoices):
    DEPARTMENT_CHAIR = auto()
    REGISTRAR = auto()
    PROFESSOR = auto()


class User(Model):
    uuid = UUIDField(primary_key=True, default=uuid4)
    email = EmailField(unique=True)
    name = CharField(max_length=255)
    auth_token = CharField(max_length=255, null=True)
    role = CharField(max_length=20, choices=UserRole.choices, default=UserRole.PROFESSOR)
