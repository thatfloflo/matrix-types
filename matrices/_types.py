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


NotGiven: Final = Sentinel("NotGiven", module_name="matrices")

MISSING: Final = Sentinel("MISSING", module_name="matrices")
"""Sentinal constant to indicate a missing value.

The `MISSING` sentinel can be used where a missing value needs to be indicated
as separate from any other object or value in Python. This is useful as a
default value where the absence of a particular value should be signified.

Importantly, comparing `MISSING` to anything other than `MISSING` itself always
evaluates to :code:`False`, so that it can be used to safely distinguish it
from the built-in :code:`None`.

Note that the type of `MISSING` is not completely unique to `MISSING` (unlike
e.g. :code:`NoneType` is to :code:`None`). This should only affect code working
with the internals of a :class:`MatrixABC` derived class or the `matrices`
package. The type is :code`matrices._types.Sentinel`, which may be shared
by other sentinel values used internally in the `matrices` package.
Therefore, using comparisons based on :code:`type()`,
:code:`issubclass()` or :code:`isinstance()` cannot be used to reliably
infer that the passed object must be `MISSING`.
"""

IndexT: TypeAlias = slice | int | tuple[int, ...]

RowColT: TypeAlias = Literal["row"] | Literal["col"]

T = TypeVar("T")

V = TypeVar("V")
