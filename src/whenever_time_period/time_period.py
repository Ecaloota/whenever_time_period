from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from plum import dispatch
from whenever import Time

from whenever_time_period.abstract import TimePeriod


@dataclass
class LinearTimePeriod(TimePeriod):
    """A LinearTimePeriod is a right-open clock interval of whenever.Time objects,
    [start_time, end_time) wherein start_time < end_time.

    Example:
    >> LinearTimePeriod(start_time=Time(5), end_time=Time(10))
    """

    def __post_init__(self):
        if not self.start_time < self.end_time:
            raise ValueError

    def __contains__(self, other: Time) -> bool:
        return self.start_time <= other < self.end_time

    @dispatch
    def __and__(self, other: LinearTimePeriod) -> Optional[LinearTimePeriod]:
        start_inter = max(self.start_time, other.start_time)
        end_inter = min(self.end_time, other.end_time)

        if start_inter < end_inter:
            return LinearTimePeriod(start_inter, end_inter)

        return None

    @dispatch
    def __and__(self, other: ModularTimePeriod) -> Optional[LinearTimePeriod]:  # noqa F811
        # two regions of possible intersection, [max(a,c), b] or [a, min(b,d)]
        # TODO Is it always true that only one OR the other intersection will occur (if any occurs)?

        # region 1
        if max(self.start_time, other.start_time) < self.end_time:
            return LinearTimePeriod(
                max(self.start_time, other.start_time), self.end_time
            )

        # region 2
        if self.start_time < min(self.end_time, other.end_time):
            return LinearTimePeriod(self.start_time, min(self.end_time, other.end_time))

        return None

    @dispatch
    def __and__(self, other: InfiniteTimePeriod) -> LinearTimePeriod:  # noqa F811
        return self


@dataclass
class ModularTimePeriod(TimePeriod):
    """A ModularTimePeriod is a right-open clock interval of whenever.Time objects,
    [start_time, end_time) wherein end_time < start_time. Used for intervals which wrap
    around midnight.

    Example:
    >> ModularTimePeriod(start_time=Time(10), end_time=Time(5))
    """

    def __post_init__(self):
        if not self.end_time < self.start_time:
            raise ValueError

    def __contains__(self, other: Time) -> bool:
        return self.start_time <= other or other < self.end_time

    @dispatch
    def __and__(self, other: LinearTimePeriod) -> Optional[LinearTimePeriod]:
        raise NotImplementedError

    @dispatch
    def __and__(self, other: ModularTimePeriod) -> ModularTimePeriod:  # noqa F811
        raise NotImplementedError

    @dispatch
    def __and__(self, other: InfiniteTimePeriod) -> ModularTimePeriod:  # noqa F811
        raise NotImplementedError


@dataclass
class InfiniteTimePeriod(TimePeriod):
    """An InfiniteTimePeriod is a right-open clock interval of whenever.Time objects,
    [start_time, end_time) wherein start_time == end_time. Used to represent intervals
    which span all possible clock times to nanosecond precision."""

    def __post_init__(self):
        if not self.start_time == self.end_time:
            raise ValueError

    def __contains__(self, other: Time) -> bool:
        if not isinstance(other, Time):
            return False
        return True

    @dispatch
    def __and__(self, other: LinearTimePeriod) -> LinearTimePeriod:
        raise NotImplementedError

    @dispatch
    def __and__(self, other: ModularTimePeriod) -> ModularTimePeriod:  # noqa F811
        raise NotImplementedError

    @dispatch
    def __and__(self, other: InfiniteTimePeriod) -> InfiniteTimePeriod:  # noqa F811
        raise NotImplementedError
