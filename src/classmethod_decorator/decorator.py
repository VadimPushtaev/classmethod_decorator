from typing import Callable, ParamSpec, TypeVar, Any, Protocol

CLASS = TypeVar("CLASS", bound=type)
P = ParamSpec("P")
R = TypeVar("R")


class _HasNameProtocol(Protocol):
    __name__: str


def classmethod_decorator(
    class_method: _HasNameProtocol,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(method: Callable[P, R]) -> Callable[P, R]:
        setattr(method, "__classmethod_decorator__", class_method)
        return method

    return decorator


def enable_classmethod_decorators[CLASS](klass: CLASS) -> CLASS:
    attr_name: str
    attr: Any

    for attr_name, attr in klass.__dict__.items():
        if (class_method := getattr(attr, "__classmethod_decorator__", None)) is not None:
            # find this class_method in the class
            class_method_to_be_called = getattr(klass, class_method.__name__, None)
            if class_method_to_be_called is None:
                raise AttributeError(f"Class method {class_method.__name__} not found in class {klass}")

            # check that we found the correct class method
            if class_method_to_be_called.__func__ is not class_method.__func__:
                raise AttributeError(
                    f"Class method {class_method.__name__} in class {klass} is not built from {class_method.__func__}"
                )

            # decorate
            setattr(klass, attr_name, class_method_to_be_called(attr))

    return klass
