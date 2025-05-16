# ruff: noqa: ANN201, ANN001
# TODO

from enum import Enum, auto
from typing import override

from courses_app.models import Course


class RuleSeverity(Enum):
    PREVENT = auto()  # Prevent department chairs or registrars from making this change.
    UNUSUAL = auto()  # Warn department chairs and display to registrar as unusual.
    DISCOURAGE = auto()  # Warn department chairs, but ignore it to the registrar.


class Rule:
    """
    Something to be checked whenever class creation or edits are performed.

    These are designed to either show a warning to the department chair making the edit
    (if `is_department_chair_)
    """

    severity: RuleSeverity

    def check_class(self, klass: Course) -> None:
        """
        Check that the given class meets the requirements for this rule.

        If it does, nothing will happen. If it does not, an exception will be raised.
        """


class RoomConflictRule(Rule):
    """
    A given room cannot host two classes at the exact same time.

    A possible exception could be if a course is cross-listed.
    """

    is_department_chair_error = True
    is_registrar_warning = True

    @override
    def check_class(self, klass): ...


class ProfessorConflictRule(Rule):
    """
    A given professor cannot teach two classes at the exact same time.

    A possible exception would be if a course is cross-listed.
    """

    is_department_chair_error = True
    is_registrar_warning = True

    @override
    def check_class(self, klass): ...


class ChapelConflictRule(Rule):
    """A class time cannot overlap with chapel."""

    is_department_chair_error = True
    is_registrar_error = True

    @override
    def check_class(self, klass): ...


class CommunityHoursRule(Rule):
    """A class time should not overlap the campus-wide "community hours"."""

    is_department_chair_warning = True
    is_registrar_warning = True

    COMMUNITY_HOURS_MWF = ((16, 19),)
    COMMUNITY_HOURS_TR = ((15.5, 18),)

    @override
    def check_class(self, klass): ...


class StandardStartTimesRule(Rule):
    """A class time should start at one of the rounded standard hours."""

    TIMES_MWF = frozenset((8, 9, 11, 12, 13, 14, 15))
    TIMES_TR = frozenset((8, 9.5, 11, 12.5, 14))

    @override
    def check_class(self, klass): ...
