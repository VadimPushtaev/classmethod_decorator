from typing import Callable, Self

from classmethod_decorator.decorator import enable_classmethod_decorators, classmethod_decorator


@enable_classmethod_decorators
class Dummy:
    DECORATED = []

    @classmethod
    def double(cls, method: Callable[[Self, int], int]) -> Callable[[Self, int], int]:
        cls.DECORATED.append(method)

        def decorated(self: Self, value: int) -> int:
            return 2 * method(self, value)

        return decorated

    @classmethod_decorator(double)
    def sqr(self, value: int) -> int:
        return value**2


def test_decorator() -> None:
    dummy = Dummy()
    assert dummy.sqr(2) == 4 * 2  # doubled
    assert len(Dummy.DECORATED) == 1
