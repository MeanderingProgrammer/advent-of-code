from dataclasses import dataclass, field
from typing import List, override

from language.language import Language
from pojo.day import Day


@dataclass(kw_only=True, init=False)
class Python(Language):
    name: str = field(default="python", repr=False)
    solution_file: str = field(default="solver.py", repr=False)

    @override
    def _setup_command(self) -> List[str]:
        return ["pip", "install", "-q", "-e", "commons/python"]

    @override
    def run_command(self, day: Day, run_args: List[str]) -> List[str]:
        return ["python", str(day.dir().joinpath(self.solution_file))] + run_args

    @override
    def template_processing(self, _: Day) -> None:
        # No additional template processing needed
        pass
