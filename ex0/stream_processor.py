from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

Numeric = int | float | list[int | float]
Text = str | list[str]
Log = dict[str, str] | list[dict[str, str]]


class ProcessStreamError(Exception):
    pass


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.ingested: list[tuple[int, str]] = []
        self.count: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        return self.ingested.pop(0)


class NumericProcessor(DataProcessor):

    def __init__(self) -> None:
        super().__init__()

    def ingest(self, data: Numeric) -> None:
        try:
            if not self.validate(data):
                raise TypeError("Got exception: Improper numeric data")
            if isinstance(data, list):
                for x in data:
                    self.ingested.append((self.count, str(x)))
                    self.count += 1
            else:
                self.ingested.append((self.count, str(data)))
                self.count += 1
        except TypeError as e:
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
            if isinstance(data, str):
                self.ingested.append((self.count, str(data)))
                self.count += 1
            else:
                for x in data:
                    self.ingested.append((self.count, str(x)))
                    self.count += 1
        except TypeError as e:
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

    def ingest(self, data: Log) -> None:
        if not self.validate(data):
            raise TypeError("Got exception: Improper numeric data")
        if isinstance(data, list):
            for x in data:
                self.ingested.append((self.count, str(x)))
                self.count += 1
        else:
            self.ingested.append((self.count, str(data)))
            self.count += 1

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(list(map(lambda x: isinstance(x,
                                                     dict), data))
                       )
        else:
            return isinstance(data, dict)


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")
    print("Testing Numeric Processor...")
    data = 42
    numproc = NumericProcessor()

    print(f"Trying to validate input '{data}': {numproc.validate(data)}")
    data = "Hello"
    print(f"Trying to validate input '{data}': {numproc.validate(data)}")
    data = "foo"
    print(f"Test invalid ingestion of string '{data}' without prior "
          "validation:")
    numproc.ingest(data)
    data = [1, 2, 3, 4, 5]
    print("Processing data:", data)
    numproc.ingest(data)
    print("Extracting 3 values...")
    for _ in range(3):
        output = numproc.output()
        print(f"Numeric value {output[0]}: {output[1]}")

    print("\n\nTesting Text Processor...")
    textproc = TextProcessor()

    data = 42
    print(f"Trying to validate input '{data}': {textproc.validate(data)}")

    data = ["Hello", "Nexus", "World"]
    print("Processing data:", data)
    textproc.ingest(data)
    print("Extracting 1 value...")
    output = textproc.output()
    print(f"Text value {output[0]}: {output[1]}")

    print("\n\nTesting Log Processor...")
    logproc = LogProcessor()

    data = "Hello"
    print(f"Trying to validate input '{data}': {logproc.validate(data)}")

    data = [{'log_level': 'NOTICE', 'log_message':
            'Connection to server'}, {'log_level': 'ERROR', 'log_message':
            'Unauthorized access!!'}]
    print("Processing data:", data)
    logproc.ingest(data)
    print("Extracting 2 values...")
    for _ in range(2):
        output = logproc.output()
        print(f"Log entry {output[0]}: {output[1]}")

if __name__ == "__main__":
    main()
