## Script derived from the vide https://www.youtube.com/watch?v=C2w45qRc3aU&t=365s
## credits goes to video's author


from dataclasses import dataclass


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
square(square(2)) 
add_one(5)

