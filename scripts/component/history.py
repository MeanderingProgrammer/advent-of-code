import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pojo.runtime_info import RuntimeInfo


@dataclass(frozen=True)
class History:
    name: Literal["all", "slow"]

    def save(self, runtimes: list[RuntimeInfo]) -> None:
        with open(f"{self.name}.json", "w") as f:
            value = [runtime.as_dict() for runtime in runtimes]
            f.write(json.dumps(value))

    def load(self, fail: bool) -> list[RuntimeInfo]:
        file = Path(f"{self.name}.json")
        if not file.is_file() and fail:
            raise Exception(f"Looks like {self.name} runtimes were never created")
        # Default to an empty list if user does not want to fail on missing data
        if not file.is_file():
            return []

        runtimes: list[RuntimeInfo] = []
        for runtime in json.loads(file.read_text()):
            runtime_info = RuntimeInfo.from_dict(runtime)
            runtimes.append(runtime_info)
        return runtimes
