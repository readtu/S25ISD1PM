"""Module for implementing Ellucian Banner API integration."""

from collections.abc import Callable, Iterable
from datetime import UTC, date, datetime, timedelta
from functools import wraps
from logging import DEBUG, basicConfig, getLogger
from threading import Thread
from typing import Any, Self

from django.conf import settings
from requests import Session, post

from chairs_project.utils import DAYS_OF_WEEK_NAME, DaysOfWeek
from courses_app.models import Course, Section
from departments_app.models import Subject
from locations_app.models import Building, Room
from semesters_app.models import Semester

from uuid import UUID

ELLUCIAN_URL = "https://integrate.elluciancloud.com"


class BannerClient:
    """A client for interacting with the Ellucian Banner API."""

    progress: float = 1
    timeout: int = 10
    progress_handlers: list[Callable[[Self], None]]
    last_authenticated: datetime | None = None
    authentication_expires: timedelta = timedelta(minutes=1)

    def __init__(self):
        """Initialize an Ellucian Banner client."""
        self.session = Session()
        self.logger = getLogger("urllib3")
        self.progress_handlers = []
        if settings.DEBUG:
            basicConfig()
            self.logger.setLevel(DEBUG)

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

    def _handle_progress(self, progress: float) -> None:
        self.progress = progress
        if settings.DEBUG:
            self.logger.info("%2f%%", self.progress * 100)
        for handler in self.progress_handlers:
            handler(self)

    def _paginate(
        self,
        *args,
        page_size: int | None = None,
        maximum: int | None = None,
        **kwargs: Any,
    ) -> Iterable[dict]:
        params = kwargs.pop("params", {})
        offset: int = 0
        while True:
            if maximum:
                self._handle_progress(offset / maximum)
            else:
                self._handle_progress(0)
            params["offset"] = str(offset)
            if page_size:
                params["limit"] = str(page_size)
            try:
                self.smart_authenticate()
                response = self.session.get(*args, **kwargs, params=params)
                json = response.json()
                _maximum = response.headers.get("x-hedtech-totalcount", "")
                # If this request probably was not supposed to be paginated
                if not _maximum:
                    break
                # If we specified no other maximum
                if not maximum:
                    maximum = int(_maximum)
                offset += len(json)
                yield from json
                if maximum and offset >= maximum:
                    break
            except KeyboardInterrupt:
                break
        if maximum:
            self._handle_progress(offset / maximum)
        else:
            self._handle_progress(1)

    @_check_authentication
    def get_resources(self) -> list[str]:
        return [
            resource["resourceName"]
            for resource in self.session.get(f"{ELLUCIAN_URL}/appconfig").json()["ownerOverrides"]
        ]

    def get_resource(self, resource: str, **kwargs: Any) -> Iterable[dict[str, Any]]:
        if settings.DEBUG:
            assert resource in self.get_resources(), (
                f"{resource} is not an available Banner resource"
            )
        yield from self._paginate(f"{ELLUCIAN_URL}/api/{resource}", **kwargs)

    def get_buildings(self, **kwargs: Any) -> Iterable[dict[str, Any]]:
        yield from self.get_resource("buildings", **kwargs)

    def get_rooms(self, **kwargs: Any) -> Iterable[dict[str, Any]]:
        yield from self.get_resource("rooms", **kwargs)

    def get_subjects(self, **kwargs: Any) -> Iterable[dict[str, Any]]:
        yield from self.get_resource("subjects", **kwargs)

    def get_sections(self, **kwargs: Any) -> Iterable[dict[str, Any]]:
        yield from self.get_resource("section-schedule-information", **kwargs)

    def get_semesters(self, **kwargs: Any) -> Iterable[dict[str, Any]]:
        yield from self.get_resource("academic-periods", **kwargs)

    def get_courses(self, **kwargs: Any) -> Iterable[dict[str, Any]]:
        yield from self.get_resource("courses", **kwargs)


class BannerResources:
    def __init__(self):
        self.client = BannerClient()

    def get_buildings(self, **kwargs: Any) -> Iterable[Building]:
        return (
            Building(
                uuid=building["id"].replace("-", ""),
                name=building["title"],
                code=building["code"],
            )
            for building in self.client.get_buildings(**kwargs)
        )

    def get_rooms(self, **kwargs: Any) -> Iterable[Room]:
        for room in self.client.get_rooms(**kwargs):
            try:
                yield Room(
                    uuid=room["id"].replace("-", ""),
                    building=Building.objects.get(uuid=room["building"]["id"].replace("-", "")),
                    number=room["number"],
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

    def get_subjects(self, **kwargs: Any) -> Iterable[Subject]:
        return (
            Subject(
                uuid=subject["id"].replace("-", ""),
                name=subject["title"],
                code=subject["abbreviation"],
            )
            for subject in self.client.get_subjects(**kwargs)
        )

    def get_courses(self, **kwargs: Any) -> Iterable[Course]:
        for course in self.client.get_courses(**kwargs):
            yield Course(
                uuid=course["id"],
                subject=Subject.objects.get(uuid=course["subject"]["id"]),
                name=course["title"].strip(),
                number=course["number"],
            )

    def get_semesters(self, **kwargs: Any) -> Iterable[Semester]:
        periods = self.client.get_semesters(**kwargs)

        semesters = {
            period["id"]: Semester(
                uuid=period["id"],
                title=period["title"],
                start = datetime.fromisoformat(period["startOn"]).date(),
                end = datetime.fromisoformat(period["endOn"]).date(),
                type=period["category"]["type"],
            )
            for period in periods
        }

        # Set the parents for the periods being generated.
        # This has to be done in a separate pass because
        # it's not guaranteed that we have constructed the parents
        # before we reach their children.
        for period in periods:
            parent_id_str = period["category"].get("parent", {}).get("id")
            if parent_id_str:
                parent_id = UUID(parent_id_str)
                child_id = UUID(period["id"])
                semesters[child_id].parent = semesters.get(parent_id)

        yield from semesters.values()


    def get_sections(self, **kwargs: Any) -> Iterable[Section]:
        for section in self.client.get_sections(**kwargs):
            try:
                events = section["instructionalEvents"]
                assert len(events) == 1, f"Can only store 1 event per section, not {len(events)}"
                event = events[0]
                repeat_type = event["recurrenceRepeatRuleType"]
                assert repeat_type == "weekly", f"Can only store weekly events, not {repeat_type}"
                days_of_week = [
                    str(DAYS_OF_WEEK_NAME.index(DaysOfWeek[day.upper()]))
                    for day in event.get("recurrenceRepeatRuleDaysOfWeek", [])
                ]
                start_date = datetime.fromisoformat(event["recurrenceStartOn"])
                start_time = start_date.time()
                end_date = datetime.fromisoformat(event["recurrenceEndOn"])
                end_time = end_date.time()

                room = Room.objects.get(
                    uuid=event["locations"][-1]["locationRoomId"].replace("-", ""),
                )
                yield Section(
                    uuid=section["sectionsId"],
                    course=Course.objects.get(uuid=section["courseId"]),
                    room=room,
                    semester=Semester.objects.get(uuid=section["sectionReportingAcademicPeriodId"]),
                    capacity=room.maximum_capacity,
                    days_of_week="".join(days_of_week),
                    start_time=start_time,
                    end_time=end_time,
                )
            except (
                Subject.DoesNotExist,
                Room.DoesNotExist,
                Course.DoesNotExist,
                KeyError,
                IndexError,
                AssertionError,
            ) as e:
                print(repr(e))


def create_task(
    banner_client: BannerClient,
    result: list,
    progress_callback: Callable[[BannerClient], None],
):
    def accumulate_result():
        result.extend(banner_client.get_buildings())

    banner_client.progress_handlers.append(progress_callback)
    thread = Thread(target=accumulate_result)
    thread.start()
    return thread


def populate():
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
    Semester.objects.all().delete()
    Semester.objects.bulk_create(br.get_semesters())
    Section.objects.all().delete()
    Section.objects.bulk_create(br.get_sections())
    
