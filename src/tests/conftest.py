from pytest import Metafunc

from tests.generators import Generators, ParametrizedArgs

GeneratorRegister: dict[str, ParametrizedArgs] = {
    "TestTimePeriod.test_time_period_construction": Generators.time_period_construction_cases(),
    "TestTimePeriod.test_time_period_membership": Generators.time_period_membership_cases(),
    "TestTimePeriod.test_time_period_linear_intersection_cases": Generators.time_period_linear_intersection_cases(),
    "TestTimePeriod.test_time_period_modular_intersection_cases": Generators.time_period_modular_intersection_cases(),
    "TestTimePeriod.test_time_period_infinite_intersection_cases": Generators.time_period_infinite_intersection_cases(),
}


def pytest_generate_tests(metafunc: Metafunc):
    if metafunc.function.__qualname__ in GeneratorRegister:
        pargs = GeneratorRegister[metafunc.function.__qualname__]
        metafunc.parametrize(pargs.argnames, pargs.funcargs)
