from uuid import uuid4

from django.db.models import Model
from django.db.models.fields import CharField, SlugField, TextField, UUIDField
from django.urls import reverse


class Article(Model):
    uuid = UUIDField(primary_key=True, default=uuid4)
    title = CharField(max_length=255)
    slug = SlugField(max_length=255)
    description = TextField(max_length=500, null=True)
    text = TextField(max_length=3000)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("view_article", kwargs={"slug": self.slug})
