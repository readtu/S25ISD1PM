"""Module for implementing Ellucian Banner API integration."""

from collections.abc import Iterable
from datetime import UTC, date, datetime, timedelta
from functools import wraps
from logging import DEBUG, basicConfig, getLogger
from typing import Any, Self

from django.conf import settings
from requests import Session, post

from classes_app.models import Class
from departments_app.models import Department, Subject
from locations_app.models import Building, Room
from semesters_app.models import Semester, Term

ELLUCIAN_URL = "https://integrate.elluciancloud.com"


class BannerClient:
    """A client for interacting with the Ellucian Banner API."""

    timeout = 10
    last_authenticated: datetime | None = None
    authentication_expires: timedelta = timedelta(minutes=1)

    def __init__(self):
        """Initialize an Ellucian Banner client."""
        self.session = Session()
        self.logger = getLogger("requests.packages.urllib3")
        if settings.DEBUG:
            basicConfig()
            getLogger("urllib3").setLevel(DEBUG)

    def authenticate(self) -> None:
        response = post(
            f"{ELLUCIAN_URL}/auth",
            headers={
                "Authorization": f"Bearer {settings.BANNER_API_KEY}",
            },
            timeout=self.timeout,
        )
        self.session.headers["Authorization"] = f"Bearer {response.text}"
        self.last_authenticated = datetime.now(tz=UTC)

    def smart_authenticate(self) -> None:
        if (
            self.last_authenticated is None
            or (datetime.now(tz=UTC) - self.last_authenticated).seconds
            > self.authentication_expires.seconds
        ):
            self.authenticate()

    @staticmethod
    def _check_authentication(function):  # noqa: ANN001
        @wraps(function)
        def decorated(self: Self, *args, **kwargs):  # noqa: ANN002, ANN003
            nonlocal function
            self.smart_authenticate()
            return function(self, *args, **kwargs)

        return decorated

    def _paginate(
        self,
        *args,
        page_size: int | None = None,
        maximum: int | None = None,
        **kwargs: Any,
    ):
        output = []
        params = kwargs.pop("params", {})
        offset: int = 0
        while True:
            params["offset"] = str(offset)
            if page_size:
                params["limit"] = str(page_size)
            try:
                self.smart_authenticate()
                response = self.session.get(*args, **kwargs, params=params)
            except KeyboardInterrupt:
                break
            json = response.json()
            length = len(json)
            if not length:
                break
            output.extend(json)
            _maximum = response.headers.get("x-hedtech-totalcount", "")
            if not maximum and _maximum:
                maximum = int(_maximum)
            offset += length
            if maximum and offset >= maximum:
                break
        return output

    @_check_authentication
    def get_resources(self) -> list[str]:
        return [
            resource["resourceName"]
            for resource in self.session.get(f"{ELLUCIAN_URL}/appconfig").json()["ownerOverrides"]
        ]

    def get_resource(self, resource: str, **kwargs: Any) -> list[dict[str, Any]]:
        if settings.DEBUG:
            assert resource in self.get_resources()
        return self._paginate(f"{ELLUCIAN_URL}/api/{resource}", **kwargs)

    def get_buildings(self, **kwargs: Any) -> list[dict[str, Any]]:
        return self.get_resource("buildings", **kwargs)

    def get_rooms(self, **kwargs: Any) -> list[dict[str, Any]]:
        return self.get_resource("rooms", **kwargs)

    def get_subjects(self, **kwargs: Any) -> list[dict[str, Any]]:
        return self.get_resource("subjects", **kwargs)

    def get_sections(self, **kwargs: Any) -> list[dict[str, Any]]:
        return self.get_resource("section-schedule-information", **kwargs)


class BannerResources:
    def __init__(self):
        self.client = BannerClient()

    def get_buildings(self, **kwargs: Any) -> list[Building]:
        return [
            Building(
                uuid=building["id"].replace("-", ""),
                name=building["title"],
                code=building["code"],
            )
            for building in self.client.get_buildings(**kwargs)
        ]

    def get_rooms(self, **kwargs: Any) -> Iterable[Room]:
        for room in self.client.get_rooms(**kwargs):
            try:
                yield Room(
                    uuid=room["id"].replace("-", ""),
                    building=Building.objects.get(uuid=room["building"]["id"].replace("-", "")),
                    code=room["number"],
                    name=room.get("title", None),
                    default_capacity=int(
                        room["occupancies"][-1]["maxOccupancy"] if "occupancies" in room else 0,
                    ),
                    maximum_capacity=int(
                        room["occupancies"][-1]["maxOccupancy"] if "occupancies" in room else 0,
                    ),
                )
            except Building.DoesNotExist:
                pass

    def get_subjects(self, **kwargs: Any) -> list[Subject]:
        return [
            Subject(
                uuid=subject["id"].replace("-", ""),
                name=subject["title"],
                code=subject["abbreviation"],
                department=Department.objects.first(),
            )
            for subject in self.client.get_subjects(**kwargs)
        ]

    def get_classes(self, **kwargs: Any) -> Iterable[Class]:
        for section in self.client.get_sections(**kwargs):
            try:
                yield Class(
                    name=section["courseTypeTitles"][-1]["typeValue"],
                    subject=Subject.objects.get(code=section["subjectAbbreviation"]),
                    code=section["courseNumber"],
                    room=Room.objects.get(
                        uuid=section["instructionalEvents"][-1]["locations"][-1][
                            "locationRoomId"
                        ].replace("-", ""),
                    ),
                    semester=Semester.objects.get_or_create(
                        start=date.fromisoformat(section["sectionStartOn"]),
                        end=date.fromisoformat(section["sectionEndOn"]),
                        defaults={
                            "year": section["sectionStartOn"].split("-", 2)[0],
                            "term": Term.FALL,
                        },
                    )[0],
                )
            except (Subject.DoesNotExist, Room.DoesNotExist, KeyError, IndexError) as e:
                pass


def populate():
    assert settings.DEBUG
    br = BannerResources()
    Building.objects.all().delete()
    Building.objects.bulk_create(br.get_buildings())
    Subject.objects.all().delete()
    Subject.objects.bulk_create(br.get_subjects())
    Room.objects.all().delete()
    Room.objects.bulk_create(br.get_rooms())
    Semester.objects.all().delete()
    Class.objects.all().delete()
    Class.objects.bulk_create(br.get_classes())
