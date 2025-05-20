"""Module for implementing Ellucian Banner API integration."""

from collections.abc import Callable, Iterable
from datetime import UTC, datetime, timedelta
from functools import wraps
from http import HTTPStatus
from logging import DEBUG, basicConfig, getLogger
from threading import Thread
from typing import Any, Self
from uuid import UUID

from django.conf import settings
from requests import Session, post

from chairs_project.utils import DAYS_OF_WEEK_NAME, DaysOfWeek
from courses_app.models import Course, Section
from departments_app.models import Subject
from locations_app.models import Building, Room
from periods_app.models import Period

ELLUCIAN_URL = "https://integrate.elluciancloud.com"


class BannerClient:
    """A client for interacting with the Ellucian Banner API."""

    progress: float = 1
    timeout: int = 10
    progress_handlers: list[Callable[[Self], None]]
    last_authenticated: datetime | None = None
    authentication_expires: timedelta = timedelta(minutes=1)

    def __init__(self) -> None:
        """Initialize an Ellucian Banner client."""
        self.session = Session()
        self.logger = getLogger("urllib3")
        self.progress_handlers = []
        if settings.DEBUG:
            basicConfig()
            self.logger.setLevel(DEBUG)

    def authenticate(self) -> None:
        """
        Authenticate into Banner.

        Stores the authentication into the HTTP Headers for future requests.
        """
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
        """Call `authenticate()` only if it hasn't been done recently."""
        if (
            self.last_authenticated is None
            or (datetime.now(tz=UTC) - self.last_authenticated).seconds
            > self.authentication_expires.seconds
        ):
            self.authenticate()

    @staticmethod
    def _check_authentication(function):  # noqa: ANN001
        """A decorator for BannerClient methods that makes the method authenticate beforehand."""

        @wraps(function)
        def decorated(self: Self, *args, **kwargs):  # noqa: ANN002, ANN003
            nonlocal function
            self.smart_authenticate()
            return function(self, *args, **kwargs)

        return decorated

    def _handle_progress(self, progress: float) -> None:
        """Report progress information whenever we find out more about it."""
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
        """
        For an endpoint that is paginated using HeadTech, continuously consume
        each page until no more are available.

        Arguments:
            page_size: the number of items to request at a time.
                If not present, the maximum page size possible,
                as determined from the expected headers, is used.
            maximum: a maximum item count to stop consum at.
                If not present, all items are consumed.
        """
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

    def get_periods(self, **kwargs: Any) -> Iterable[dict[str, Any]]:
        yield from self.get_resource("academic-periods", **kwargs)

    def get_courses(self, **kwargs: Any) -> Iterable[dict[str, Any]]:
        yield from self.get_resource("courses", **kwargs)

    @_check_authentication
    def update_course(self, *, uuid: str | UUID, name: str | None = None):
        data = {}
        if name is not None:
            data["title"] = str(name)
        assert data, "No changes specified"
        response = self.session.get(f"{ELLUCIAN_URL}/api/courses/{uuid}").json()
        data["subject"] = response["subject"]
        data["credits"] = [{"minimum": response["credits"][0]["minimum"]}]
        response = self.session.put(
            f"{ELLUCIAN_URL}/api/courses/{uuid}",
            json=data,
        )
        assert response.status_code == HTTPStatus.OK, response.text


class BannerResources:
    """A client for fetching Chairs resources from Banner."""

    def __init__(self) -> None:
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

    def update_course(self, course: Course, name: str | None = None) -> None:
        self.client.update_course(uuid=course.uuid, name=name)

    def get_courses(self, **kwargs: Any) -> Iterable[Course]:
        for course in self.client.get_courses(**kwargs):
            yield Course(
                uuid=course["id"],
                subject=Subject.objects.get(uuid=course["subject"]["id"]),
                name=course["title"].strip(),
                number=course["number"],
            )

    def get_periods(self, **kwargs: Any) -> Iterable[Period]:
        periods = list(self.client.get_periods(**kwargs))

        periods_map = {
            period["id"]: Period(
                uuid=period["id"],
                title=period["title"],
                start=datetime.fromisoformat(period["startOn"]).date(),
                end=datetime.fromisoformat(period["endOn"]).date(),
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
                parent_id = parent_id_str
                child_id = period["id"]
                periods_map[child_id].parent = periods_map.get(parent_id)

        yield from periods_map.values()

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
                    period=Period.objects.get(uuid=section["sectionReportingAcademicPeriodId"]),
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
