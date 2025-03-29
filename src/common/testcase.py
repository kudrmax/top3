from dataclasses import dataclass, is_dataclass, fields
from typing import Any


@dataclass(frozen=True)
class TestCaseBase:
    def get_data(self) -> tuple[Any, ...]:
        if not is_dataclass(self):
            raise TypeError("Объект, который наследуется от TestCaseBase должен использоваться с @dataclass")
        return tuple(getattr(self, field.name) for field in fields(self))
