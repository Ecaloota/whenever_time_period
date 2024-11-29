from dataclasses import dataclass

from whenever import Time

from whenever_time_period.time_period import TimePeriod


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

    def __and__(self, other: TimePeriod) -> TimePeriod | None:
        raise NotImplementedError

    # def normalise(self) -> list[TimePeriod]:
    #     """Normalise a LinearTimePeriod into constituent TimePeriod(s) such that each period
    #     has start_time < end_time.

    #     Example:
    #     >> LinearTimePeriod(Time(5), Time(10)).normalise()
    #     >> [LinearTimePeriod(Time(5), Time(10))]
    #     """
    #     return [self]
