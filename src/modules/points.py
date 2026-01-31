from typing import Callable
from PySimpleEvents import Event

__points = [0]

on_gain = Event[[int], None]()
on_loss = Event[[int], None]()
on_change = Event[[int], None]()

def sum(n: int = 1) -> None:
    on_gain.emit(n)
    __points[0] += n

def sub(n: int = 1) -> None:
    on_loss.emit(n)
    __points[0] -= n

def get() -> int:
    return __points[0]

def set(n: int) -> None:
    on_change.emit(n)
    __points[0] = n

def reset() -> None:
    on_change.emit(0)
    __points[0] = 0

def query(expr: Callable[[int], bool]) -> bool:
    return expr(__points[0])

def query_eval(expr: Callable[[int], int]) -> int:
    return expr(__points[0])

def eval(expr: Callable[[int], int]) -> None:
    return set(expr(__points[0]))