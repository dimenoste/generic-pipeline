## Script derived from the vide https://www.youtube.com/watch?v=C2w45qRc3aU&t=365s
## credits goes to video's author


from dataclasses import dataclass
from typing import Callable



@dataclass
class NumberWithLogs:
    result: int
    logs: list

def square(x: int) -> int:
    return x*x

def add_one(x: int) -> int:
    return x + 1


def square(x: int) -> NumberWithLogs:
    result = x * x
    logs = [f"Squared {x} to get {x * x}"]
    return NumberWithLogs(result, logs)


def add_one(x: NumberWithLogs) -> NumberWithLogs:
    x.logs.append(f"Added 1 to {x.result} to get {x.result + 1}")
    x.result = x.result + 1
    return x


print(add_one(square(2))) # result = 5
print(add_one(square(2)).result) # result = 5
print(add_one(square(2)).logs) # result = 5


# Issues because we treat NumberWithLogs as an int or vice versa
# square(square(2)) 
# add_one(5)


# New function 
def wrap_with_logs(x: int) -> NumberWithLogs:
    return NumberWithLogs(x, [])


# Tweaked Square Function
def square(x: NumberWithLogs) -> NumberWithLogs:
    log_str = f"Squared {x.result} to get {x.result * x.result}"
    x.result = x.result * x.result
    x.logs.append(log_str)
    return x


def add_one(x: NumberWithLogs) -> NumberWithLogs:
    log_str = f"Added 1 to {x.result} to get {x.result + 1}"
    x.result = x.result + 1
    x.logs.append(log_str)
    return x

def multiply_by_three(x: NumberWithLogs) -> NumberWithLogs:
    log_str = f"Added 1 to {x.result} to get {x.result + 1}"
    x.result = x.result + 1
    x.logs.append(log_str)
    return x


# New Call Pattern
print(square(square(wrap_with_logs(2))))

print(add_one(wrap_with_logs(5)))


## Run With Logs function

def run_with_logs(input: NumberWithLogs,
                  transform: Callable[[int], NumberWithLogs]) -> NumberWithLogs:
    
    new_nbr_with_logs = transform(input.result)
    return NumberWithLogs(new_nbr_with_logs.result,
                          input.logs + new_nbr_with_logs.logs) 


a = wrap_with_logs(5)


print(run_with_logs(3))

a = wrap_with_logs(5)
b = run_with_logs(a, add_one)
c = run_with_logs(b, square)
d = run_with_logs(c, multiply_by_three)





