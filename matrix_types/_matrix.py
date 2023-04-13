"""Mutable 2-dimensional matrix type."""
from __future__ import annotations
from typing import Any, Callable, Self, Sequence

from ._base import MatrixABC
from ._types import T, V, RowColT, IndexT


class Matrix(MatrixABC[T]):
    """Abstract base class for 2-dimensional matrix types."""

    # SHAPE MANIPULATION

    def transpose(self) -> Self:
        self._transpose()
        return self

    def resize(self, rows: int | tuple[int, int], cols: int | None) -> Self:
        self._resize(rows, cols)
        return self

    def flip(self, *, by: RowColT = "row") -> Self:
        self._flip(by=by)
        return self

    def insertrow(self, index: int, data: Sequence[T]) -> Self:
        self._insertrow(index, data)
        return self

    def insertcol(self, index: int, data: Sequence[T]) -> Self:
        self._insertcol(index, data)
        return self

    def delrow(self, index: int) -> Self:
        self._delrow(index)
        return self

    def delcol(self, index: int) -> Self:
        self._delcol(index)
        return self

    def swaprows(self, a_index: int, b_index: int) -> Self:
        self._swaprows(a_index, b_index)
        return self

    def swapcols(self, a_index: int, b_index: int) -> Self:
        self._swapcols(a_index, b_index)
        return self

    # MATRIX OPERATIONS

    def imatadd(self, other: MatrixABC[V]) -> Self | Matrix[V]:
        self._imatadd(other)
        return self

    def imatsub(self, other: MatrixABC[V]) -> Self | Matrix[V]:
        self._imatsub(other)
        return self

    def imatmul(self, other: MatrixABC[V]) -> Self | Matrix[V]:
        self._imatmul(other)
        return self

    def iscaladd(self, scalar: V) -> Self | Matrix[V]:
        self._iscaladd(scalar)
        return self

    def iscalsub(self, scalar: V) -> Self | Matrix[V]:
        self._iscalsub(scalar)
        return self

    def iscalmul(self, scalar: V) -> Self | Matrix[V]:
        self._iscalmul(scalar)
        return self

    def map(
        self,
        func: Callable[..., V],
        *args: Any,
        **kwargs: Any
    ) -> Self | Matrix[V]:
        self._map(func, *args, **kwargs)
        return self

    # DATA GETTERS AND SETTERS

    def __setitem__(self, key: tuple[IndexT, IndexT], value: T) -> None:
        raise NotImplementedError()

    def __delitem__(self, key: tuple[IndexT, IndexT]) -> None:
        self.__setitem__(key, self._default)

    # DUNDER METHODS

    def __iadd__(self, other: MatrixABC[V] | T) -> Self | Matrix[V]:
        if isinstance(other, MatrixABC):
            return self.imatadd(other)
        return self.iscaladd(other)

    def __isub__(self, other: MatrixABC[V] | T) -> Self | Matrix[V]:
        if isinstance(other, MatrixABC):
            return self.imatsub(other)
        return self.iscalsub(other)

    def __imul__(self, other: V) -> Self | Matrix[V]:
        return self.iscalmul(other)

    def __imatmul__(self, other: MatrixABC[V]) -> Self | Matrix[V]:
        return self.imatmul(other)
