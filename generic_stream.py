from __future__ import annotations
from abc import ABC, abstractmethod
import collections
from typing import Any, Callable, TypeVar



T = TypeVar("T", bound=collections.abc.Iterable)
type U = int | str


class DataProcessor[T:U](ABC):
    @staticmethod
    @abstractmethod
    def process(data: T[U]) -> T[U]:
        pass

    @staticmethod
    @abstractmethod
    def validate(data: T[U]) -> bool:
        pass

    def format_output(event: str, state: str) -> None:
        print(f"Output: {event} : {state}")




class NumProcessor(DataProcessor[T[int]]):
    def process(data: int) -> int:
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


print(NumProcessor.process([2]))


print(process[2])