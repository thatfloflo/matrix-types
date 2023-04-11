"""Immutable 2-dimensional matrix type."""
from __future__ import annotations
from typing import Any, Callable, Self, Sequence

from ._base import MatrixABC
from ._types import T, V, RowColT


class FrozenMatrix(MatrixABC[T]):
    """Abstract base class for 2-dimensional matrix types."""

    # SHAPE MANIPULATION

    def transpose(self) -> Self:
        new = self.copy()
        new._transpose()
        return new

    def resize(self, rows: int | tuple[int, int], cols: int | None) -> Self:
        new = self.copy()
        new._resize(rows, cols)
        return new

    def flip(self, *, by: RowColT = "row") -> Self:
        new = self.copy()
        new._flip(by=by)
        return new

    def insertrow(self, index: int, data: Sequence[T]) -> Self:
        new = self.copy()
        new._insertrow(index, data)
        return new

    def insertcol(self, index: int, data: Sequence[T]) -> Self:
        new = self.copy()
        new._insertcol(index, data)
        return new

    def delrow(self, index: int) -> Self:
        new = self.copy()
        new._delrow(index)
        return new

    def delcol(self, index: int) -> Self:
        new = self.copy()
        new._delcol(index)
        return new

    def swaprows(self, a_index: int, b_index: int) -> Self:
        new = self.copy()
        new._swaprows(a_index, b_index)
        return new

    def swapcols(self, a_index: int, b_index: int) -> Self:
        new = self.copy()
        new._swapcols(a_index, b_index)
        return new

    # MATRIX OPERATIONS

    def map(
        self,
        func: Callable[..., V],
        *args: Any,
        **kwargs: Any
    ) -> Self | FrozenMatrix[V]:
        new = self.copy()
        new._map(func, *args, **kwargs)
        return new
