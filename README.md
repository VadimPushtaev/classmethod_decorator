# Classmethod Decorators

A small Python hack that allows using a `@classmethod` within the same class as a decorator for other methods in the same class, which is not typically possible because functions are turned into methods once the class definition is complete.

## Installation

```bash
pip install classmethod_decorators
```

# Usage

```python
from typing import Callable
from typing_extensions import Self
from classmethod_decorators import enable_classmethod_decorators, classmethod_decorator

@enable_classmethod_decorators
class Foo:
    @classmethod
    def register(cls, method: Callable[[Self], None]) -> Callable[[Self], None]:
        print(f"{method} is registered")

        def decorated(self: Self) -> None:
            print(f"decorated {method}")
            method(self)

        return decorated

    @classmethod_decorator(register)
    def method(self) -> None:
        print("method")

Foo().method()
```
