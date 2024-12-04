import random
from contextlib import nullcontext
from dataclasses import dataclass

import pytest
from whenever import Time

from tests.utils import TestUtils
from whenever_time_period.time_period import (
    InfiniteTimePeriod,
    LinearTimePeriod,
    ModularTimePeriod,
)


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

    def time_period_linear_intersection_cases() -> ParametrizedArgs:
        """Generate relevant cases to assert the correctness of the intersections between two TimePeriods,
        where at least the first TimePeriod is a LinearTimePeriod

        Relevant cases are:

        1. Linear
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

        2. Modular
        2.1 Total disjoint
            |---|
        ----|   |----

        2.2 Left overhang
              |----|
        ----|   |----

        2.3 Right overhang
         |----|
        ----|   |----

        2.4 Complete overlap
              |---|
        -|   |-------

        2.5. Double overlap
          |------------|
        -----|      |-----

        3. Infinite
        3.1 Infinite case
            |---|
        -----|-----
        """

        cases = [
            (  # 1.1.
                LinearTimePeriod(Time(5), Time(10)),
                LinearTimePeriod(Time(12), Time(15)),
                None,
            ),
            (  # 1.2.
                LinearTimePeriod(Time(5), Time(10)),
                LinearTimePeriod(Time(8), Time(12)),
                LinearTimePeriod(Time(8), Time(10)),
            ),
            (  # 1.3.
                LinearTimePeriod(Time(8), Time(12)),
                LinearTimePeriod(Time(5), Time(10)),
                LinearTimePeriod(Time(8), Time(10)),
            ),
            (  # 1.4.
                LinearTimePeriod(Time(8), Time(10)),
                LinearTimePeriod(Time(8), Time(10)),
                LinearTimePeriod(Time(8), Time(10)),
            ),
            (  # 1.5.
                LinearTimePeriod(Time(8), Time(10)),
                LinearTimePeriod(Time(10), Time(12)),
                None,
            ),
            (  # 1.6.
                LinearTimePeriod(Time(10), Time(12)),
                LinearTimePeriod(Time(8), Time(10)),
                None,
            ),
            (  # 2.1.
                LinearTimePeriod(Time(5), Time(10)),
                ModularTimePeriod(Time(10), Time(5)),
                None,
            ),
            (  # 2.2.
                LinearTimePeriod(Time(5), Time(10)),
                ModularTimePeriod(Time(7), Time(4)),
                LinearTimePeriod(Time(7), Time(10)),
            ),
            (  # 2.3.
                LinearTimePeriod(Time(5), Time(10)),
                ModularTimePeriod(Time(12), Time(7)),
                LinearTimePeriod(Time(5), Time(7)),
            ),
            (  # 2.4.
                LinearTimePeriod(Time(5), Time(8)),
                ModularTimePeriod(Time(4), Time(1)),
                LinearTimePeriod(Time(5), Time(8)),
            ),
            (  # 2.5.
                LinearTimePeriod(Time(3), Time(10)),
                ModularTimePeriod(Time(7), Time(5)),
                [
                    LinearTimePeriod(Time(3), Time(5)),
                    LinearTimePeriod(Time(7), Time(10)),
                ],
            ),
            (  # 3.1.
                LinearTimePeriod(Time(5), Time(10)),
                InfiniteTimePeriod(Time(5), Time(5)),
                LinearTimePeriod(Time(5), Time(10)),
            ),
        ]

        return ParametrizedArgs(
            argnames=["period_a", "period_b", "expected_intersection"], funcargs=cases
        )

    def time_period_modular_intersection_cases() -> ParametrizedArgs:
        """Generate relevant cases to assert the correctness of the intersections between two TimePeriods,
        where at least the first TimePeriod is a ModularTimePeriod

        Relevant cases are:

        1. Linear
        1.1. Total disjoint
        ----|   |---
            |---|

        1.2. Left overhang
        ----|   |---
              |---|

        1.3. Right overhang
        ----|   |---
          |---|

        1.4. Complete overlap
        -|   |-------
               |---|

        1.5. Double overlap
        -----|      |-----
          |------------|

        2. Modular
        2.1. Complete overlap
        ----|   |----
        --|       |--

        2.2. Left overlap
        ----|   |----
        --|   |----

        2.3. Right overlap
        ----|   |----
        ------|   |--

        3. Infinite
        3.1. Modular + Infinite
        ----|   |----
        ------|------
        """

        cases = [
            (  # 1.1.
                ModularTimePeriod(Time(10), Time(5)),
                LinearTimePeriod(Time(5), Time(10)),
                None,
            ),
            (  # 1.2.
                ModularTimePeriod(Time(10), Time(5)),
                LinearTimePeriod(Time(7), Time(12)),
                LinearTimePeriod(Time(10), Time(12)),
            ),
            (  # 1.3.
                ModularTimePeriod(Time(10), Time(5)),
                LinearTimePeriod(Time(3), Time(7)),
                LinearTimePeriod(Time(3), Time(5)),
            ),
            (  # 1.4.
                ModularTimePeriod(Time(10), Time(5)),
                LinearTimePeriod(Time(11), Time(13)),
                LinearTimePeriod(Time(11), Time(13)),
            ),
            (  # 1.5.
                ModularTimePeriod(Time(7), Time(5)),
                LinearTimePeriod(Time(3), Time(10)),
                [
                    LinearTimePeriod(Time(3), Time(5)),
                    LinearTimePeriod(Time(7), Time(10)),
                ],
            ),
            (  # 2.1.
                ModularTimePeriod(Time(10), Time(5)),
                ModularTimePeriod(Time(11), Time(4)),
                ModularTimePeriod(Time(11), Time(4)),
            ),
            (  # 2.2.
                ModularTimePeriod(Time(10), Time(5)),
                ModularTimePeriod(Time(8), Time(3)),
                ModularTimePeriod(Time(10), Time(3)),
            ),
            (  # 2.3.
                ModularTimePeriod(Time(10), Time(5)),
                ModularTimePeriod(Time(12), Time(7)),
                ModularTimePeriod(Time(12), Time(5)),
            ),
            (  # 3.1.
                ModularTimePeriod(Time(10), Time(5)),
                InfiniteTimePeriod(Time(11), Time(11)),
                ModularTimePeriod(Time(10), Time(5)),
            ),
        ]

        return ParametrizedArgs(
            argnames=["period_a", "period_b", "expected_intersection"], funcargs=cases
        )

    def time_period_infinite_intersection_cases() -> ParametrizedArgs:
        """Generate relevant cases to assert the correctness of the intersections between two TimePeriods,
        where at least the first TimePeriod is an InfiniteTimePeriod

        Relevant cases are:

        1. Linear
        -----|-----
            |---|

        2. Modular
        -----|-----
        --|     |--

        3. Infinite
        -----|-----
        -----|-----
        """

        cases = [
            (
                InfiniteTimePeriod(Time(1), Time(1)),
                LinearTimePeriod(Time(5), Time(8)),
                LinearTimePeriod(Time(5), Time(8)),
            ),
            (
                InfiniteTimePeriod(Time(1), Time(1)),
                ModularTimePeriod(Time(8), Time(5)),
                ModularTimePeriod(Time(8), Time(5)),
            ),
            (
                InfiniteTimePeriod(Time(1), Time(1)),
                InfiniteTimePeriod(Time(5), Time(5)),
                InfiniteTimePeriod(Time(5), Time(5)),
            ),
            (  # special case, note that InfiniteTimePeriod[1, 1) == InfiniteTimePeriod[5, 5)
                InfiniteTimePeriod(Time(1), Time(1)),
                InfiniteTimePeriod(Time(5), Time(5)),
                InfiniteTimePeriod(Time(1), Time(1)),
            ),
        ]

        return ParametrizedArgs(
            argnames=["period_a", "period_b", "expected_intersection"], funcargs=cases
        )
