from pathlib import Path
from typing import Any, Callable, Type, cast
import importlib.util
import sys


def require(path: str | Path) -> dict[str, Any]:
    path = Path(path).resolve()

    if not path.exists():
        raise FileNotFoundError(path)

    module_name = path.stem

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Não foi possível carregar {path}")

    module = importlib.util.module_from_spec(spec)

    # opcional: evita recarregar se já existir
    sys.modules[module_name] = module

    spec.loader.exec_module(module)

    return module.__dict__

class ModuleResult[P]:
    def __init__(self, value: P) -> None:
        self.value = value

    def get(self) -> Any:
        return ~self
    
    def set(self, value: Any) -> None:
        self.value = value

    def __invert__(self) -> Any:
        return self.value
    
    def __matmul__[T](self, other: Type[T]) -> T :
        return cast(T, self.value)
    
    def __lshift__(self, other: Any):
        self.set(other)

    def __getattr__(self, name):
        return ModuleResult(getattr(self.get(), name))

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if isinstance(self.get(), Callable):
            return self.get()(*args, **kwds)
        else:
            return ModuleResult(getattr(self.get(), "__call__")(*args, **kwds))

    def __str__(self) -> str:
        return str(self.get())
    
    def type(self) -> Type[P]:
        return type(self.get())

    def shift(self) -> P:
        return cast(P, self)


class Module:
    def __init__(self, path: str | Path) -> None:
        self.data = require(path)

    def get(self, name: str) -> ModuleResult:
        return ModuleResult(self.data[name])