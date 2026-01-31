from PySimpleEvents import Event
_health = [5]

on_damage = Event[[int], None]()
on_heal = Event[[int], None]()
on_change = Event[[int], None]()

def damage(n: int = 1) -> None:
    on_damage.emit(n)
    _health[0] -= n

def heal(n: int = 1) -> None:
    on_heal.emit(n)
    _health[0] += n

def set(n: int) -> None:
    on_change.emit(n)
    _health[0] = n

def reset() -> None:
    on_change.emit(5)
    _health[0] = 5

def get() -> int:
    return _health[0]
