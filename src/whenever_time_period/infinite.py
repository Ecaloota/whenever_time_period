from dataclasses import dataclass

from whenever import Time

from whenever_time_period.time_period import TimePeriod


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

    def __and__(self, other: TimePeriod) -> TimePeriod | None:
        raise NotImplementedError

    # def normalise(self) -> list[TimePeriod]:
    #     """Normalise an InfiniteTimePeriod into constituent TimePeriod(s).
    #     Calling normalise on an InfiniteTimePeriod returns the InfiniteTimePeriod centered at Time.MIDNIGHT.

    #     Example:
    #     >> InfiniteTimePeriod(Time(10), Time(10))
    #     >> [InfiniteTimePeriod(Time.MIDNIGHT, Time.MIDNIGHT)]
    #     """
    #     return [InfiniteTimePeriod(Time.MIDNIGHT, Time.MIDNIGHT)]
