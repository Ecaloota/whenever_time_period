from dataclasses import dataclass

from whenever import Time

from whenever_time_period.linear import LinearTimePeriod
from whenever_time_period.time_period import TimePeriod


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
