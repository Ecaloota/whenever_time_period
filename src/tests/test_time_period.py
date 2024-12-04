from typing import Any, Optional

from whenever import Time

from whenever_time_period.abstract import AbstractTimePeriod
from whenever_time_period.time_period import (
    InfiniteTimePeriod,
    LinearTimePeriod,
    ModularTimePeriod,
)


class TestTimePeriod:
    def test_time_period_construction(
        self,
        subcls: AbstractTimePeriod,
        start_time: object,
        end_time: object,
        context: Any,
    ) -> None:
        """Assert that it is possible to construct (only) valid instances of a AbstractTimePeriod, or otherwise
        that the appropriate Exception is raised"""

        with context:
            inst = subcls(start_time, end_time)
            assert inst.start_time == start_time and inst.end_time == end_time

    def test_time_period_membership(
        self, period: AbstractTimePeriod, candidate_time: Time, is_expected_member: bool
    ) -> None:
        """Assert that a given candidate time object is either in the period defined by the given Period if expected,
        or otherwise that it is not, if not expected"""

        assert (candidate_time in period) is is_expected_member

    def test_time_period_linear_intersection_cases(
        self,
        period_a: LinearTimePeriod,
        period_b: AbstractTimePeriod,
        expected_intersection: Optional[LinearTimePeriod] | LinearTimePeriod,
    ) -> None:
        """TODO"""

        assert (period_a & period_b) == expected_intersection

    def test_time_period_modular_intersection_cases(
        self,
        period_a: ModularTimePeriod,
        period_b: AbstractTimePeriod,
        expected_intersection: Optional[LinearTimePeriod] | ModularTimePeriod,
    ) -> None:
        """TODO"""

        assert (period_a & period_b) == expected_intersection

    def test_time_period_infinite_intersection_cases(
        self,
        period_a: InfiniteTimePeriod,
        period_b: AbstractTimePeriod,
        expected_intersection: AbstractTimePeriod,
    ) -> None:
        """TODO"""

        assert (period_a & period_b) == expected_intersection
