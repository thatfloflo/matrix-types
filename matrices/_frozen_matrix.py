"""Immutable 2-dimensional matrix type."""
from __future__ import annotations
from typing import Any, Callable, Self, Sequence

from ._base import MatrixABC
from ._types import T, V, RowColT


class FrozenMatrix(MatrixABC[T]):
    """Immutable 2-dimensional Matrix type.

    Behaves almost identically to the mutable :class:`Matrix` type, but where
    :class:`Matrix` instances are modified in place, it instead returns an
    immutable copy of :class:`FrozenMatrix` with the function applied instead.

    :class:`FrozenMatrix` also misses all the 'in-situ' methods of
    :class:`Matrix`, that is operations typically prefixed with :code:`i` such
    as :func:`Matrix.iscaladd()` and :func:`Matrix.imatmul()`, as well as their
    operator equivalents (e.g. :code:`+=` and :code:`@=`).

    .. important::

        It is important to note that :class:`FrozenMatrix` is *imperfectly
        immutable*.

        While :class:`FrozenMatrix` does not provide any public functionality
        that would alter a specific instance of :class:`FrozenMatrix`, and all
        operations affecting values or shape result in copies, once
        instantiated, Python itself does not prevent user code from modifying
        the internals of an object (e.g. by accessing and modifying the
        internal data structure directly). This means that immutability with
        :class:`FrozenMatrix` can be assumed, but not guaranteed.
    """

    # SHAPE MANIPULATION

    def transpose(self) -> Self:
        new = self.copy()
        new._transpose()
        return new

    def resize(self, rows_or_shape: int | tuple[int, int], cols: int | None = None) -> Self:
        new = self.copy()
        new._resize(rows_or_shape, cols)
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

    def removerow(self, index: int) -> Self:
        new = self.copy()
        new._removerow(index)
        return new

    def removecol(self, index: int) -> Self:
        new = self.copy()
        new._removecol(index)
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
