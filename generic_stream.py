from __future__ import annotations
from abc import ABC, abstractmethod
import collections
from typing import Any, Callable, TypeVar



class StreamProcessorError(Exception):
    pass

class ProcessStepError(StreamProcessorError):
    def __init__(self, reason):
        super().__init__()
        self.reason = reason

    def log(self):
        return super().__str__(f"{self.type(ProcessStepError).__name__}"
                               f": {self.reason}")


T = TypeVar("T", bound=collections.abc.Iterable)


class DataProcessor[T](ABC):
    # def __init__(self, data, event, state):
    #     super().__init__()
    #     self. data = data
    #     self.event = event
    #     self.state = state


    @abstractmethod
    def process(data: list[T]) -> list[T]:
        return [x * 2 for x in data]

    @abstractmethod
    def validate(data: list[T]) -> bool:
        pass

    def format_output(event: str, state: str) -> None:
        print(f"Output: {event} : {state}")




class NumProcessor(DataProcessor):
    def process(data: list[int]) -> list[int]:
        return [x * 2 for x in data]

    def validate(data):
        return isinstance(data, list) and all([isinstance(x, int)
                                               for x in data])

class TextProcessor(DataProcessor):
    def process(data: list[str]) -> list[str]:
        return [x.capitalize() for x in data]

    def validate(data):
        return isinstance(data, list) and all([isinstance(x, str)
                                               for x in data])




proc = DataProcessor

print(DataProcessor.process([1,2,3]))




print(NumProcessor.process([1,2,3]))
print(NumProcessor.process(["df", "de"]))
print(TextProcessor.process(["abc", "gdje", "de"]))




print(list.__mro__)
print(tuple.__mro__)
print(set.__mro__)