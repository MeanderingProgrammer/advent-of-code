from typing import Any, Protocol


class Command(Protocol):
    def info(self) -> dict[str, Any]: ...

    def run(self) -> None: ...
