from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, NotRequired, TypedDict
from .common import getjson


root = Path(".").resolve() / "data/"
class TQuestionEvent(TypedDict):
    success: str
    failed: str

class TQuestion(TypedDict):
    type: NotRequired[Literal["literal"]] # default: 'literal'
    name: str
    answer: str
    retry: NotRequired[bool]
    tries: NotRequired[int]
    on: NotRequired[TQuestionEvent]

class TTag(TypedDict):
    values: list[str]

class TTags(TypedDict):
    questions: NotRequired[TTag]

class TPack(TypedDict):
    name: str
    format: int
    description: NotRequired[str]
    version: NotRequired[str]

class TEvent(TypedDict):
    require: NotRequired[list[str]]
    run: list[str]

@dataclass
class ResourceLocation:
    np: str
    name: str
    def __str__(self) -> str:
        return f"{self.np}:{self.name}"

def get_res_loc(res_loc: str) -> ResourceLocation:
    np, name = res_loc.split(':')
    return ResourceLocation(np, name)

Packages: dict[str, Any] = {}
class Pack:
    def __init__(self, pack: "PackManager", name: str) -> None:
        self.fp = pack.fp / (name)
        self.np = name
    
    def get_questions(self) -> dict[str, TQuestion]:
        _questions = self.fp / "questions/"
        qs = {}
        if _questions.exists():
            for f in _questions.iterdir():
                qs[f.stem] = getjson(f)
        
        return qs
    
    def get_tags(self) -> TTags:
        _tags = self.fp / "tags/"
        t = TTags()
        if _tags.exists():
            for f in _tags.iterdir():
                t[f.stem] = getjson(f)
        return t
    
    def get_pack(self) -> TPack:
        return getjson(self.fp / "pack.json")
    
    def get_events(self) -> dict[str, TEvent]:
        _events = self.fp / "events/"
        e = {}
        if _events.exists():
            for f in _events.iterdir():
                e[f.stem] = getjson(f)
        return e
    
    def run_event(self, name: str, packages: dict[str, dict[str, Any]] = Packages):
        event = self.get_events()[name]
        run = event['run']
        requirements = event.get('require', [])
        data = {}
        for requirement in requirements:
            data[requirement] = packages[requirement]

        script = '\n'.join(run)
        exec(script, data)
        
class PackFormatError(Exception):
    def __init__(self, current: int, minimum: int | None = None, maximum: int | None = None) -> None:
        if not minimum and not maximum:
            raise Exception("Pack format is not supported")
        if not minimum and maximum:
            raise Exception(f"Pack format {current} is not supported. Must be below {maximum}")
        if not maximum and minimum:
            raise Exception(f"Pack format {current} is not supported. Must be atleast {minimum}")
        raise Exception(f"Pack format {current} is not supported. Must be between {minimum} and {maximum}")

class PackManager:
    def __init__(self) -> None:
        self.fp = root

        self.packs = dict[str, Pack]()
    
    def get(self, name: str) -> Pack:
        return self.packs[name]
    
    def get_question(self, res_loc: str) -> TQuestion:
        np, name = res_loc.split(':')
        return self.packs[np].get_questions()[name]
    
    def get_tag(self, res_loc: str) -> TTag:
        np, name = res_loc.split(':')
        return self.packs[np].get_tags()[name]
    
    def get_pack(self, name: str) -> TPack:
        return self.packs[name].get_pack()

    def iter(self):
        for p in self.packs.values():
            yield p
    
    def load(self):
        for f in self.fp.iterdir():
            self.packs[f.stem] = Pack(self, f.stem)

    def get_all_questions(self) -> dict[str, TQuestion]:
        qs = {}
        for p in self.iter():
            qs.update({f"{p.np}:{k}": v for k, v in p.get_questions().items()})
        return qs
    
    def get_all_tags(self) -> dict[str, TTag]:
        t = {}
        for p in self.iter():
            t.update({f"{p.np}:{k}": v for k, v in p.get_tags().items()})
        return t
    
    def get_event(self, res_loc: str) -> TEvent:
        np, name = res_loc.split(':')
        if (f:=self.get_pack(np)['format']) != 2: 
            raise PackFormatError(f, 2)
        return self.packs[np].get_events()[name]
    
    def get_all_events(self) -> dict[str, TEvent]:
        e = {}
        for p in self.iter():
            e.update({f"{p.np}:{k}": v for k, v in p.get_events().items()})
        return e
    
    def run_event(self, res_loc: str, packages: dict[str, dict[str, Any]] = Packages):
        np, name = res_loc.split(':')
        self.packs[np].run_event(name, packages)