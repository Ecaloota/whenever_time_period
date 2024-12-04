# WheneverTimePeriods

**An unofficial extension of the [whenever](https://github.com/ariebovenberg/whenever) library supporting abstract time periods!**

## Overview
`WheneverTimePeriods` builds on the `whenever` library by introducing basic support for **TimePeriods** -- abstract intervals of the form `[a, b)`, where **a** and **b** are `whenever.Time` clock times.

`WheneverTimePeriods` introduces support for the following kinds of time periods:

* **LinearTimePeriod**: `[a, b)`, where `a < b`. Used to represent standard clock periods such as [05:00, 07:00).

* **ModularTimePeriod**: `[a, b)`, where `a > b`. Used to represent clock periods that wrap around midnight. For example, [23:00, 04:00).
* **InfiniteTimePeriod**: `[a, b)`, where `a = b`. Used to represent clock periods that span all possible clock times.

## Features
* **Flexible time periods**: Handles both standard time periods and time periods that cross midnight or span all clock times.

* **Highly Extensible**: We define an abstract `TimePeriod` ABC class that is designed to be extensible for your TimePeriod requirements. All required methods are defined using multiple dispatch, thanks to the `plum` library. Adding support for new TimePeriod subclasses is as simple as registering new signatures.

## Installation

`# TODO Put on pypi`

## Quickstart

### Define a TimePeriod

```python3
from whenever import Time
from whenever_time_period.time_period import LinearTimePeriod, ModularTimePeriod, InfiniteTimePeriod

linear_period = LinearTimePeriod(Time(3), Time(10))
modular_period = ModularTimePeriod(Time(7), Time(5))
infinite_period = InfiniteTimePeriod(Time(5), Time(5))

"""
For example:

               3    5      7    10
               |    |      |    |

Linear:        |----------------)
Modular:     >------)      [------->
Infinite:    >------[-------------->
"""

```

### Intersection between TimePeriods

```python3
>> linear_period & modular_period
[LinearTimePeriod(Time(3), Time(5)), LinearTimePeriod(Time(7), Time(10))]

# same as above
>> modular_period & linear_period
LinearTimePeriod(Time(7), Time(10))

>> infinite_period & linear_period
LinearTimePeriod(Time(3), Time(10))

>> infinite_period & modular_period
ModularTimePeriod(Time(7), Time(5))
```

### Time Membership

```python3
# TimePeriods are left-closed
>> Time(3) in linear_period
True

# TimePeriods are right-open
>> Time(10) in linear_period
False

# All Times are members of InfiniteTimePeriods
>> Time(7) in InfiniteTimePeriod
True
```

## Contributing

Contributions are welcome. Contributions should be accompanied by a well-documented pull request and appropriate testing.