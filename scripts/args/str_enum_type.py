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
        value = super().convert(value=value, param=param, ctx=ctx)
        if value is None:
            return None
        return self.enum_type(value)
