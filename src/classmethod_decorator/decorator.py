from dataclasses import dataclass
from functools import wraps
from typing import Callable, ParamSpec, TypeVar, Any, Protocol, Generic, cast

from classmethod_decorator.exceptions import ClassNotDecoratedError

CLASS = TypeVar("CLASS", bound=type)
P = ParamSpec("P")
R = TypeVar("R", covariant=True)


class _ClassMethod(Protocol):
    __name__: str


@dataclass(kw_only=True, frozen=True)
class _WrappedMethod(Generic[P, R]):
    wrapped: Callable[P, R]
    class_method: _ClassMethod

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        raise ClassNotDecoratedError(
            f"Class method {self.wrapped.__name__} was decorated with @classmethod_decorator, "
            f"but the class does not support classmethod decorators."
        )


def classmethod_decorator(
    class_method: _ClassMethod,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(method: Callable[P, R]) -> Callable[P, R]:
        # We cannot expose that the actual type is _WrappedMethod,
        # because it should soon become a method again and must look like a method from the outside.
        return cast(Callable[P, R], _WrappedMethod(wrapped=method, class_method=class_method))

    return decorator


def enable_classmethod_decorators[CLASS](klass: CLASS) -> CLASS:
    attr_name: str
    attr: Any

    for attr_name, attr in klass.__dict__.items():
        if isinstance(attr, _WrappedMethod):
            class_method = attr.class_method
            # find this class_method in the class
            class_method_to_be_called = getattr(klass, class_method.__name__, None)
            if class_method_to_be_called is None:
                raise AttributeError(f"Class method {class_method.__name__} not found in class {klass}")

            # We cannot make it part of the interface, so let's require in runtime
            if not hasattr(class_method, "__func__"):
                raise AttributeError(f"Class method {class_method.__name__} in class {klass} is not a class method")

            # check that we found the correct class method
            if class_method_to_be_called.__func__ is not class_method.__func__:
                raise AttributeError(
                    f"Class method {class_method.__name__} in class {klass} is not built from {class_method.__func__}"
                )

            # decorate
            setattr(klass, attr_name, wraps(attr.wrapped)(class_method_to_be_called(attr.wrapped)))

    return klass
