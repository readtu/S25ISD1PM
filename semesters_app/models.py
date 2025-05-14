# ruff: noqa: D105

from collections.abc import Iterable
from uuid import uuid4

from django.db.models import Model, SET_NULL
from django.db.models.enums import TextChoices
from django.db.models.fields import DateField, UUIDField, CharField
from django.db.models.fields.related import ForeignKey
from django.urls import reverse


class PeriodTypes(TextChoices):
    YEAR = "year"
    TERM = "term"
    SUBTERM = "subterm"


class Semester(Model):
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

    class Meta:
        ordering = ["parent__uuid", "start"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("view_semester", kwargs={"uuid": self.uuid})
