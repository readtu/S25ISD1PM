"""Rules for auditing classes and class conflicts."""

# ruff: noqa: ANN201, ANN001

from typing import override

from courses_app.models import Section

RULES = list[type["Rule"]]()


class Rule:
    """Something to be checked whenever class creation or edits are performed."""

    def __init_subclass__(cls) -> None:
        RULES.append(cls)

    @classmethod
    def check_section(cls, section: Section) -> None:
        """
        Check that the given class meets the requirements for this rule.

        If it does, nothing will happen. If it does not, an exception will be raised.
        """


class RoomConflictRule(Rule):
    """
    A given room cannot host two classes at the exact same time.

    A possible exception could be if a course is cross-listed.
    """

    @override
    @classmethod
    def check_section(cls, section): ...


class ProfessorConflictRule(Rule):
    """
    A given professor cannot teach two classes at the exact same time.

    A possible exception would be if a course is cross-listed.
    """

    @override
    @classmethod
    def check_section(cls, section): ...


class ChapelConflictRule(Rule):
    """A class time cannot overlap with chapel."""

    @override
    @classmethod
    def check_section(cls, section):
        this_start = section.start_time.hour + section.start_time.minute / 60
        if set(section.days_of_week) & set("024") and 10 <= this_start < 11:
            raise AssertionError("Section overlaps with chapel.")


class CommunityHoursRule(Rule):
    """A class time should not overlap the campus-wide "community hours"."""

    COMMUNITY_HOURS_MWF = ((16, 19),)
    COMMUNITY_HOURS_TR = ((15.5, 18),)

    @override
    @classmethod
    def check_section(cls, section):
        this_start = section.start_time.hour + section.start_time.minute / 60
        this_end = section.end_time.hour + section.end_time.minute / 60
        if set(section.days_of_week) & set("024"):
            for block_start, block_end in cls.COMMUNITY_HOURS_MWF:
                if block_start <= this_start <= block_end or block_end <= this_end <= block_end:
                    raise AssertionError("Section overlaps with community hours.")
        if set(section.days_of_week) & set("13"):
            for block_start, block_end in cls.COMMUNITY_HOURS_TR:
                if block_start <= this_start <= block_end or block_end <= this_end <= block_end:
                    raise AssertionError("Section overlaps with community hours.")


class StandardStartTimesRule(Rule):
    """A class time should start at one of the rounded standard hours."""

    TIMES_MWF = frozenset((8, 9, 11, 12, 13, 14, 15))
    TIMES_TR = frozenset((8, 9.5, 11, 12.5, 14))

    @override
    @classmethod
    def check_section(cls, section):
        this_start = section.start_time.hour + section.start_time.minute / 60
        if set(section.days_of_week) & set("024") and this_start not in cls.TIMES_MWF:
            raise AssertionError("Section does not start at standard time.")
        if set(section.days_of_week) & set("13") and this_start not in cls.TIMES_TR:
            raise AssertionError("Section does not start at standard time.")
