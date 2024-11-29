import random
from contextlib import nullcontext
from dataclasses import dataclass

import pytest
from whenever import Time

from tests.utils import TestUtils
from whenever_time_period.infinite import InfiniteTimePeriod
from whenever_time_period.linear import LinearTimePeriod
from whenever_time_period.modular import ModularTimePeriod


@dataclass
class ParametrizedArgs:
    argnames: list[str]
    funcargs: list[tuple]


class Generators:
    def time_period_construction_cases() -> ParametrizedArgs:
        """Generate relevant cases to assert that TimePeriod subclass instance construction
        is valid given valid inputs, or otherwise that the appropriate exception is
        raised"""

        cases = [
            # linear cases
            (LinearTimePeriod, Time(0), Time(1), nullcontext(None)),
            (LinearTimePeriod, Time(1), Time(0), pytest.raises(ValueError)),
            (LinearTimePeriod, Time(1), Time(1), pytest.raises(ValueError)),
            # modular cases
            (ModularTimePeriod, Time(0), Time(1), pytest.raises(ValueError)),
            (ModularTimePeriod, Time(1), Time(0), nullcontext(None)),
            (ModularTimePeriod, Time(1), Time(1), pytest.raises(ValueError)),
            # infinite cases
            (InfiniteTimePeriod, Time(0), Time(1), pytest.raises(ValueError)),
            (InfiniteTimePeriod, Time(1), Time(0), pytest.raises(ValueError)),
            (InfiniteTimePeriod, Time(1), Time(1), nullcontext(None)),
        ]

        return ParametrizedArgs(
            argnames=["subcls", "start_time", "end_time", "context"],
            funcargs=cases,
        )

    def time_period_membership_cases() -> ParametrizedArgs:
        """Generate relevant cases to assert that a given Time is contained within
        the period defined by a TimePeriod subclass"""

        start_int, end_int = TestUtils.generate_integers(2, 0, 23, min_gap=3)
        start_time, end_time = Time(start_int), Time(end_int)

        # given an interval [a, b) where a < b and b-a >= 3 and a,b in [0, 23],
        # some value C is in [a, b) when a <= C < b. (Cond. 1)
        # likewise, C is not in [a, b) when 0 <= C < a OR b <= C <= 23 (Cond. 2)
        member_candidate_a_lt_b = Time(
            random.randint(start_int, end_int - 1)
        )  # by Cond. 1
        non_member_a_lt_b = Time(
            random.choice(
                [
                    random.randint(0, start_int - 1),
                    random.randint(end_int, Time.MAX.hour),
                ]
                if start_int != 0
                else [random.randint(end_int, Time.MAX.hour)]
            )
        )  # by Cond. 2

        # given an interval [a, b) where b < a and (23-a)+b >= 3 and a,b in [0, 23],
        # some value C is in [a, b) when a <= C <= 23 AND 0 <= C < b (Cond. 3)
        # likewise, C is not in [a, b) when b <= C < a. (Cond. 4)
        member_candidate_a_gt_b = Time(
            random.choice(
                [
                    random.randint(end_int, Time.MAX.hour),
                    random.randint(0, start_int - 1),
                ]
                if start_int != 0
                else [random.randint(end_int, Time.MAX.hour)]
            )
        )  # by Cond. 3

        non_member_a_gt_b = Time(
            random.randint(start_int, end_int - 1)
        )  # by Cond. 4, end_int != 0

        cases = [
            # LinearTimePeriod cases
            (  # candidate time in period
                LinearTimePeriod(start_time, end_time),
                member_candidate_a_lt_b,
                True,
            ),
            (  # candidate time not in period
                LinearTimePeriod(start_time, end_time),
                non_member_a_lt_b,
                False,
            ),
            (  # candidate time in period, c == start_time
                LinearTimePeriod(start_time, end_time),
                start_time,
                True,
            ),
            (  # candidate time not in period, c == end_time (False)
                LinearTimePeriod(start_time, end_time),
                end_time,
                False,
            ),
            # InfiniteTimePeriod cases
            (  # all candidate times in period
                InfiniteTimePeriod(start_time, start_time),
                end_time,
                True,
            ),
            (  # all candidate times in period
                InfiniteTimePeriod(start_time, start_time),
                start_time,
                True,
            ),
            # ModularTimePeriod cases
            (  # candidate_time in period
                ModularTimePeriod(end_time, start_time),
                member_candidate_a_gt_b,
                True,
            ),
            (  # candidate time not in period
                ModularTimePeriod(end_time, start_time),
                non_member_a_gt_b,
                False,
            ),
            (  # candidate time not in period, c == start_time
                ModularTimePeriod(end_time, start_time),
                start_time,
                False,
            ),
            (  # candidate time in period, c == end_time
                ModularTimePeriod(end_time, start_time),
                end_time,
                True,
            ),
        ]

        return ParametrizedArgs(
            argnames=["period", "candidate_time", "is_expected_member"], funcargs=cases
        )

    def time_period_normalise_cases() -> ParametrizedArgs:
        """Generate relevant cases to ensure we correctly normalise all instances of
        ModularTimePeriod"""

        cases = [
            (
                Time(10),
                Time(5),
                [
                    LinearTimePeriod(Time.MIDNIGHT, Time(5)),
                    LinearTimePeriod(Time(10), Time.MAX),
                ],
            ),
            (
                Time.MAX,
                Time(5),
                [
                    LinearTimePeriod(Time.MIDNIGHT, Time(5)),
                    Time.MAX,
                ],
            ),
            (
                Time(5),
                Time.MIDNIGHT,
                [
                    Time.MIDNIGHT,
                    LinearTimePeriod(Time(5), Time.MAX),
                ],
            ),
            (
                Time.MAX,
                Time.MIDNIGHT,
                [Time.MAX],
            ),
        ]

        return ParametrizedArgs(
            argnames=["start_time", "end_time", "expected_periods"],
            funcargs=cases,
        )

    def time_period_finite_non_wrapped_intersection_cases() -> ParametrizedArgs:
        """Generate relevant cases to assert the correctness of the intersection between two
        valid finite TimePeriod instances that do not wrap around MIDNIGHT.

        Relevant cases are:

        1.1. No intersection
            |-----|     |-----|

        1.2. Right intersection
            |-----|
                |-----|

        1.3. Left intersection
            |-----|
        |-----|

        1.4. Total intersection
            |-----|
            |-----|

        1.5. Right-touching intersection (no intersection)
            |-----|
                  |-----|

        1.6. Left-touching intersection (no intersection)
            |-----|
        |---|
        """

        pass

    def time_period_finite_wrapped_intersection_cases() -> ParametrizedArgs:
        """Generate relevant cases to assert the correctness of the intersection between two
        valid finite TimePeriod instances that wrap around MIDNIGHT.

        Relevant cases are:

        2.1

        2.2

        2.3

        2.4

        """

        pass

    def time_period_finite_wrapped_non_wrapped_intersection_cases() -> ParametrizedArgs:
        """Generate relevant cases to assert the correctness of the intersection between two
        valid finite TimePeriod instances, one of which wraps around MIDNIGHT, and the other which does not.

        Relevant cases are:

        3.1

        3.2

        3.3

        """

        pass

    def time_period_infinite_intersection_cases() -> ParametrizedArgs:
        """Generate relevant cases to assert the correctness of the intersection between two
        valid TimePeriod instances, at LEAST one of which is NOT finite.

        4.1

        4.2

        4.3

        """
