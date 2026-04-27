from __future__ import annotations
from abc import ABC, abstractmethod
import collections
from typing import Any, Callable, Generic, TypeVar, Union

from typing import Sequence


U = TypeVar("U", int, str)


class DataProcessor(ABC, Generic[U]):
    @abstractmethod
    @staticmethod
    def process(data: Sequence[U]) -> Sequence[U]:
        pass

    @abstractmethod
    @staticmethod
    def validate(data: Sequence[U]) -> bool:
        pass

    @staticmethod
    def format_output(event: str, state: str) -> None:
        print(f"Output: {event} : {state}")


class NumProcessor(DataProcessor[int]):
    @staticmethod
    def process(data: list[int]) -> list[int]:
        return [x * 2 for x in data]

    @staticmethod
    def validate(data: list[int]) -> bool:
        return isinstance(data, list) and all([isinstance(x, int)
                                               for x in data])


class TextProcessor(DataProcessor[str]):
    @staticmethod
    def process(data: list[str]) -> list[str]:
        return [x.capitalize() for x in data]

    @staticmethod
    def validate(data: list[str]) -> bool:
        return isinstance(data, list) and all([isinstance(x, str)
                                               for x in data])


print(NumProcessor.process([2]))
