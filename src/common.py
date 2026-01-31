import json
from pathlib import Path
from typing import Any


def getjson(p: str | Path):
    return json.loads(Path(p).read_text())
def setjson(d: Any, p: str | Path):
    return json.dump(d, Path(p).open("w+"), indent=4)
datapacks = Path(".").resolve() / "data/"