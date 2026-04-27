from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar, Callable, Self, Union
from typing import Generic, TypeVar




# A monad is defined as a monoid in the category of endofunctors, 
# meaning it is an endofunctor (a functor mapping a category to itself) 
# equipped with two natural transformations that satisfy monoid laws. 
# Specifically, a monad consists of an endofunctor $T$,
# a unit transformation $\eta$ (often called return or unit),
# and a multiplication transformation $\mu$ (often called join or flatMap).



class ErrorPipeline(Exception):
    pass

######## Pipeline Monad
# T = "raw type"
T = TypeVar('T')
S = TypeVar('S')

## Wrapper Type
# Result<T> = "wrapped type"


class Result(Generic[T, S]):
    def __init__(self, value: Optional[T], error: Optional[ErrorPipeline]):
        self.value = value
        self.error = error

    @classmethod
    def flatmap(self, transform: Callable[[Union[T, S]], Union[T, S]]) -> Self:
        if self.value is None:
            return Self
        return transform(self.value)


def to_option(x: T) -> Result:
    if x % 2 == 0:
        return Result(value=x, error=None)
    else:
        return Result(value=None, error=ErrorPipeline(f"Problem : {x} is odd,"
                                                      "it should be even"))


## function steps
def square(x: T) -> T:
    return x*x


def add_one(x: T) -> T:
    return x + 1


res = to_option(12).flatmap(square).flatmap(add_one)
print(res)


