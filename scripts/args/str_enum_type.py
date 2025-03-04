from enum import StrEnum
from typing import Any, Type, override

import click


class StrEnumType(click.Choice):
    name = "str enum"

    def __init__(self, enum_type: Type[StrEnum]):
        super().__init__(choices=[element.value for element in enum_type])
        self.enum_type: Type[StrEnum] = enum_type

    @override
    def convert(self, value: str, param, ctx) -> Any:
        result = super().convert(value=value, param=param, ctx=ctx)
        return None if result is None else self.enum_type(result)
