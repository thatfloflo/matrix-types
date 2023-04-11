"""Types for internal use with the matrices."""
from typing import TypeVar, final, Final, TypeAlias, Literal


@final
class Sentinel:

    def __init__(self, name: str, repr: str | None = None, module_name: str | None = None) -> None:
        self.name = str(name)
        self.repr = str(repr) if repr is not None else f"<{name}>"
        self.module_name = str(module_name) if module_name is not None else __name__

    def __repr__(self) -> str:
        return self.repr


NotGiven: Final = Sentinel("NotGiven", module_name="matrix_types")
MISSING: Final = Sentinel("MISSING", module_name="matrix_types")

IndexT: TypeAlias = slice | int | tuple[int, ...]
RowColT: TypeAlias = Literal["row"] | Literal["col"]
T = TypeVar("T")
V = TypeVar("V")
