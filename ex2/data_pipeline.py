from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Protocol

Numeric = int | float | list[int | float]
Text = str | list[str]
Log = dict[str, str] | list[dict[str, str]]


class ProcessStreamError(Exception):
    pass


class datasreamessor(ABC):
    def __init__(self) -> None:
        self.ingested: list[tuple[int, str]] = []
        self.count: int = 0
        self.nb_item: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        return self.ingested.pop(0)


class NumericProcessor(datasreamessor):

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
            self.nb_item += 1
        except TypeError as e:
            print(f"{e}")

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(list(map(lambda x: isinstance(x, int) or
                                isinstance(x, float), data))
                       )
        else:
            return isinstance(data, int) or isinstance(data, float)


class TextProcessor(datasreamessor):
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
            self.nb_item += 1
        except TypeError as e:
            print(f"{e}")

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(list(map(lambda x: isinstance(x,
                                                     str), data))
                       )
        else:
            return isinstance(data, str)


class LogProcessor(datasreamessor):
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
        self.nb_item += 1

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(list(map(lambda x: isinstance(x,
                                                     dict), data))
                       )
        else:
            return isinstance(data, dict)


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class DataStream():
    def __init__(self):
        self._processor_list: list[datasreamessor] = []
        self._unhandled_data: list[Any] = []
        self.len_stream: int = 0

    def register_processor(self, proc: datasreamessor) -> None:
        if isinstance(proc, datasreamessor):
            self._processor_list.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        try:
            self.len_stream = len(stream)
            for data in stream:
                for proc in self._processor_list:
                    if proc.validate(data):
                        proc.ingest(data)
                        break
                else:
                    self._unhandled_data.append(data)
        except (ProcessStreamError, TypeError) as e:
            print(e)

    def print_processors_stats(self) -> None:
        for proc in self._processor_list:
            print(f"{type(proc).__name__} : total {proc.count}"
                  "items processed, "
                  f"remaining {self.len_stream - proc.nb_item} on processor")

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processor_list:
            output_logs = []
            data = proc.ingested[:nb] if nb <= len(proc.ingested) else proc.ingested
            if isinstance(proc, LogProcessor):
                for item in range(len(data)):
                    log = data[item][1]
                    elem = log[1:-1].replace('\'', '').split(",")[0].split(":")
                    level = str(elem[1]).strip()
                    elem = log[1:-1].replace('\'', '').split(",")[1].split(":")
                    message = str(elem[1]).strip()
                    output_logs.append([item, f"{level}: {message}"])
                plugin.process_output(output_logs)
            else:
                plugin.process_output(data)


class CSV:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        data = ",".join([x[1] for x in data])
        print(data)

class JSON:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        mydict = dict()
        for item, x in enumerate(data):
            mydict[f"item_{item}"] = x[1]
        print(mydict)


if __name__ == "__main__":
    data = [
            'Hello world',
            [3.14, -1, 2.71],
            [
                {'log_level': 'WARNING',
                 'log_message': 'Telnet access! Use ssh instead'},
                {'log_level': 'INFO',
                 'log_message': 'User wil is connected'}
            ],
            ["dre2", "fr", "25", []],
            42,
            ['Hi', 'five']
        ]
    print(data)
    datasream = DataStream()
    myprocs = [NumericProcessor(), TextProcessor(), LogProcessor()]
    for proc in myprocs:
        datasream.register_processor(proc)  # type: ignore[func-returns-value]
    datasream.process_stream(data)

    datasream.print_processors_stats()
    print(f"Unhandled data : {datasream._unhandled_data}")

    nb_to_send = 3
    print(f"Send {nb_to_send} processed data from each processor to a CSV plugin:")
    csv_plugin = CSV()
    datasream.output_pipeline(2, csv_plugin)
    json_plugin = JSON()
    datasream.output_pipeline(2, json_plugin)