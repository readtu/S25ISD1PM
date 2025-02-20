from uuid import uuid4

from django.db.models import Model
from django.db.models.fields import BooleanField, CharField, UUIDField
from django.urls import reverse

# Create your models here.


class Building(Model):
    uuid = UUIDField(primary_key=True, default=uuid4)
    identifier = CharField(max_length=10, unique=True)
    name = CharField(max_length=255, unique=True)
    available = BooleanField(default=True)

    def __str__(self) -> str:
        return self.identifier

    def get_absolute_url(self) -> str:
        return reverse("view_building", kwargs={"uuid": self.uuid})
