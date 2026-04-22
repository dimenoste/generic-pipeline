from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Callable



class StreamProcessorError(Exception):
    pass

class ProcessStepError(StreamProcessorError):
    def __init__(self, reason):
        super().__init__()
        self.reason = reason

    def log(self):
        return super().__str__(f"{self.type(ProcessStepError).__name__}"
                               f": {self.reason}")


class DataProcessor(ABC):
    # def __init__(self, data, event, state):
    #     super().__init__()
    #     self. data = data
    #     self.event = event
    #     self.state = state


    @abstractmethod
    def process(data: list[Any]) -> str:
        pass

    @abstractmethod
    def validate(data: list[Any]) -> bool:
        pass

    def format_output(event: str, state: str) -> None:
        print(f"Output: {event} : {state}")


class NumericProcessor(DataProcessor):
    def process(data: list[int]) -> str:
        if not isinstance(data, list):
            raise TypeError
        try:
            str_result = ""
            if len(data) == 0:
                raise ProcessLookupError("")
            for elem in data:
                str_result += str(elem)
        except TypeError as e:
            print(f"Data should be a list of int : {e}") 
        except ProcessStepError as e:
            e.log("Data should not be empty")

    def validate(data):
        return isinstance(data, list) and all([isinstance(x, int)
                                               for x in data])


numproc = NumericProcessor.validate([1, 2, "gd"])
print(numproc)


### generic




#### Functor

class Functor:
    def __init__(self, value: Any) -> None:
        self.value = value

    def map(self, func: Callable) -> Functor:
        return Functor(func(self.value))

def add_one(x: int) -> int:
    return x + 1

def multiply_by_two(x: int) -> int:
    return x * 2


def main() -> None:
    f = Functor(5)

    ## Mapping within the same category (Functor -> Functor)
    g = f.map(add_one) # g is also a factor instance
    print(f.value)
    print(g.value)

    s = g.map(multiply_by_two)
    print(s.value)



main()