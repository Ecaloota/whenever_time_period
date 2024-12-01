from typing import Any

from whenever import Time

# from whenever_time_period import ModularTimePeriod
from whenever_time_period.abstract import TimePeriod
from whenever_time_period.time_period import LinearTimePeriod, ModularTimePeriod


class TestTimePeriod:
    def test_time_period_construction(
        self, subcls: TimePeriod, start_time: object, end_time: object, context: Any
    ) -> None:
        """Assert that it is possible to construct (only) valid instances of a TimePeriod, or otherwise
        that the appropriate Exception is raised"""

        with context:
            inst = subcls(start_time, end_time)
            assert inst.start_time == start_time and inst.end_time == end_time

    def test_time_period_membership(
        self, period: TimePeriod, candidate_time: Time, is_expected_member: bool
    ) -> None:
        """Assert that a given candidate time object is either in the period defined by the given Period if expected,
        or otherwise that it is not, if not expected"""

        assert (candidate_time in period) is is_expected_member

    def test_modular_time_period_normalise_cases(
        self,
        start_time: Time,
        end_time: Time,
        expected_periods: list[TimePeriod | Time],
    ) -> None:
        """Assert that we correctly normalise the given Period"""

        normed = ModularTimePeriod(start_time, end_time).normalise()
        for idx, np in enumerate(normed):
            assert expected_periods[idx] == np

    def test_foo(self):
        a = LinearTimePeriod(Time(5), Time(10))
        b = ModularTimePeriod(Time(10), Time(5))
        a & b
