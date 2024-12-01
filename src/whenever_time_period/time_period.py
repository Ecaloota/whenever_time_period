from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

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
    def __and__(self, other: ModularTimePeriod) -> Any:  # noqa F811
        print("foo")
        raise NotImplementedError

    @dispatch
    def __and__(self, other: InfiniteTimePeriod) -> Any:  # noqa F811
        print("wowo")
        raise NotImplementedError

    # def normalise(self) -> list[TimePeriod]:
    #     """Normalise a LinearTimePeriod into constituent TimePeriod(s) such that each period
    #     has start_time < end_time.

    #     Example:
    #     >> LinearTimePeriod(Time(5), Time(10)).normalise()
    #     >> [LinearTimePeriod(Time(5), Time(10))]
    #     """
    #     return [self]


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

    def __and__(self, other: TimePeriod) -> TimePeriod | None:
        raise NotImplementedError

    def normalise(self) -> list[Time | TimePeriod]:
        """Normalise a ModularTimePeriod into constituent LinearTimePeriod(s).

        Example:
        # start_time > end_time
        >> ModularTimePeriod(Time(10), Time(5)).normalise()
        >> [LinearTimePeriod(Time.MIDNIGHT, Time(5)), LinearTimePeriod(Time(10), Time.MAX)]

        # Special case 1: start_time == Time.MAX
        >> ModularTimePeriod(Time.MAX, Time(5)).normalise()
        >> [LinearTimePeriod(Time.MIDNIGHT, Time(5)), Time.MAX]

        # Special case 2: end_time == Time.MIDNIGHT
        >> ModularTimePeriod(Time(5), Time.MIDNIGHT).normalise()
        >> [LinearTimePeriod(Time(5), Time.MAX), Time.MAX]

        # Special case 3: start_time == Time.MAX and end_time == Time.MIDNIGHT
        >> ModularTimePeriod(Time.MAX, Time.MIDNIGHT).normalise()
        >> [Time.MAX]
        """

        # Special case 3
        if self.start_time == Time.MAX and self.end_time == Time.MIDNIGHT:
            return [Time.MAX]

        p1 = (
            LinearTimePeriod(self.start_time, Time.MAX)
            if self.start_time != Time.MAX
            else Time.MAX
        )
        p2 = (
            LinearTimePeriod(Time.MIDNIGHT, self.end_time)
            if self.end_time != Time.MIDNIGHT
            else Time.MIDNIGHT
        )

        return sorted([p1, p2])


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

    def __and__(self, other: TimePeriod) -> Optional[TimePeriod]:
        raise NotImplementedError

    # def normalise(self) -> list[TimePeriod]:
    #     """Normalise an InfiniteTimePeriod into constituent TimePeriod(s).
    #     Calling normalise on an InfiniteTimePeriod returns the InfiniteTimePeriod centered at Time.MIDNIGHT.

    #     Example:
    #     >> InfiniteTimePeriod(Time(10), Time(10))
    #     >> [InfiniteTimePeriod(Time.MIDNIGHT, Time.MIDNIGHT)]
    #     """
    #     return [InfiniteTimePeriod(Time.MIDNIGHT, Time.MIDNIGHT)]
