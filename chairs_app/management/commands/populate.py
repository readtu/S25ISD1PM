from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count

from chairs_project.banner import BannerResources
from courses_app.models import Course, Section
from departments_app.models import Subject
from locations_app.models import Building, Room
from periods_app.models import Period


class Command(BaseCommand):
    help = "Populates the local development database with data from Banner."

    def handle(self, *args: Any, **options: Any) -> None:
        if not settings.DEBUG:
            raise CommandError(
                "Population script is destructive and can only be run in development.",
            )
        assert settings.DEBUG
        br = BannerResources()

        Building.objects.all().delete()
        Building.objects.bulk_create(br.get_buildings())
        Subject.objects.all().delete()
        Subject.objects.bulk_create(br.get_subjects())
        Room.objects.all().delete()
        Room.objects.bulk_create(br.get_rooms())
        Course.objects.all().delete()
        Course.objects.bulk_create(br.get_courses())
        Period.objects.all().delete()
        Period.objects.bulk_create(br.get_periods(), ignore_conflicts=True)
        Section.objects.all().delete()
        Section.objects.bulk_create(br.get_sections())

        Building.objects.annotate(rooms__count=Count("rooms")).filter(rooms__count=0).delete()
        Period.objects.filter(type="term").annotate(
            sub_periods__count=Count("sub_periods"),
        ).filter(sub_periods__count=0).delete()
        Period.objects.filter(type="year").annotate(
            sub_periods__count=Count("sub_periods"),
        ).filter(sub_periods__count=0).delete()

        for year in Period.objects.filter(type="year"):
            year.start = min(term.start for term in year.sub_periods.all())
            year.end = max(term.end for term in year.sub_periods.all())
            year.save()
