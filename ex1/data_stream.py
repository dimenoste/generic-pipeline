from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from abc import ABC, abstractmethod
from collections.abc import Iterable

Numeric = int | float | list[int | float] | list[int] | list[float]
Text = str | list[str]
Log = dict[str, str] | list[dict[str, str]]


class ProcessStreamError(Exception):
    pass


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.ingested: list[str] = []
        self.count: int = 1

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        rank = self.count
        self.count += 1
        return (rank, self.ingested.pop(0))


class NumericProcessor(DataProcessor):

    def __init__(self) -> None:
        super().__init__()

    def ingest(self, data: Numeric) -> None:
        try:
            if not self.validate(data):
                raise TypeError("Got exception: Improper numeric data")
            if isinstance(data, Iterable):
                for x in data:
                    self.ingested.append(str(x))
            else:
                self.ingested.append(str(data))
        except TypeError as e:
            self.ingested = []
            print(f"{e}")

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(list(map(lambda x: isinstance(x, int) or
                                isinstance(x, float), data))
                       )
        else:
            return isinstance(data, int) or isinstance(data, float)


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()

    def ingest(self, data: Text) -> None:
        try:
            if not self.validate(data):
                raise TypeError("Got exception: Improper numeric data")
            for x in data:
                self.ingested.append(str(x))
        except TypeError as e:
            self.ingested = []
            print(f"{e}")

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(list(map(lambda x: isinstance(x,
                                                     str), data))
                       )
        else:
            return isinstance(data, str)


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()

    def ingest(self, data: Text) -> None:
        try:
            if not self.validate(data):
                raise TypeError("Got exception: Improper numeric data")
            for x in data:
                self.ingested.append(str(x))
        except TypeError as e:
            self.ingested = []
            print(f"Got exception: {e}")

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(list(map(lambda x: isinstance(x,
                                                     dict), data))
                       )
        else:
            return isinstance(data, dict)




class DataStream():
    _processor_list: DataProcessor = []
    validators: list[DataProcessor | None] = []

    def register_processor(self, proc: DataProcessor) -> None:
        if isinstance(proc, DataProcessor):
            self._processor_list.append(proc)
    
    def get_validators(self, stream: list[Any]) -> None:
        try:
            if not isinstance(stream, list):
                raise ProcessStreamError("Stream data should be a list")
            for data in stream:
                potential_validators = list(filter(lambda x: x.validate(data),
                                                   self._processor_list))
                if len(potential_validators) > 0:
                    first_validator = potential_validators[0]
                    self.validators.append(first_validator)
                else:
                    self.validators.append(None)
            if len(self.validators) != len(self._processor_list):
                raise ProcessStreamError("For each data, you should have a valid processor or None at this point")
            if None in self.validators:
                raise ProcessStreamError("DataStream error -"
                                         "Can't process element in stream:"
                                         f"{data}")

        except ProcessStreamError as e:
            self.validators = []
            print(e)


    def process_stream(self, stream: list[Any]) -> None:
        try:
            self.get_validators(stream)
            for proc, data in zip(self.validators, stream):
                proc.data()

        except ProcessStreamError as e:
            print(e)

    def print_processors_stats(self) -> None:
        for proc in self._processor_list:
            elem_for_proc = list(filter(lambda x: isinstance(x,
                                                    proc),
                                                    self.validators))
            
            remaining_elem = len(data) - len(numeric_elements) 
            

if __name__ == "__main__":
    data = [
            'Hello world',
            [3.14, -1, 2.71],
            [
                {'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'},
                {'log_level': 'INFO', 'log_message': 'User wil is connected'}
            ],
            42,
            ['Hi', 'five']
        ]

    dataproc = DataStream()
    myprocs = [NumericProcessor(), TextProcessor(), LogProcessor()]
    [dataproc.register_processor(proc) for proc in myprocs]
    print(dataproc._processor_list)
    dataproc.process_stream(data)
    print(dataproc.validators)

