"""Mutable 2-dimensional matrix type."""
from __future__ import annotations
from typing import Any, Callable, Self, Sequence, overload, cast, Literal

from ._base import MatrixABC
from ._types import T, V, RowColT, IndexT, NotGiven, Sentinel


class Matrix(MatrixABC[T]):
    """Mutable 2-dimensional Matrix type.

    Matrix objects can be instantiated in several different ways:

    .. py:function:: Matrix(data: MatrixT[T] [, shape: tuple[int, int], *, default: T]) -> Matrix[T]

        Initialises a new :class:`Matrix` from another :class:`MatrixT`
        instance (i.e. another :class:`Matrix` or :class:`FrozenMatrix`).

        The *shape* and *default* arguments are optional -- if omitted the
        values from the :class:`MatrixT` passed as *data* will be used.

        :Example:

            >>> m = Matrix([1, 2, 3, 4], shape=(2, 2), default=0)
            >>> print(m)
                0  1
              ┌      ┐
            0 │ 1  2 │
            1 │ 3  4 │
              └      ┘
            >>> n = Matrix(m, shape=(3, 3))  # default is inferred from m
            >>> print(n)
                0  1  2
              ┌         ┐
            0 │ 1  2  0 │
            1 │ 3  4  0 │
            2 │ 0  0  0 │
              └         ┘

    .. py:function:: Matrix(data: Sequence[Sequence[T]] [, shape: tuple[int, int]], *, default: T) -> Matrix[T]

        Initialises a new :class:`Matrix` from a sequence of sequences (e.g. a
        list of lists, or a tuple of tuples).

        The *shape* argument is optional. If provided *data* will be reshaped
        to conform to the specified *shape*, otherwise the *shape* will be
        inferred as follows: The row count equals the length of the outer
        sequence, the column count equals the length of the first subsequence.

        The *default* argument is required.

        :Example:

            >>> m = Matrix([[1, 2, 3], [4, 5, 6]], default=0)
            >>> print(m)
                0  1  2
              ┌         ┐
            0 │ 1  2  3 │
            1 │ 4  5  6 │
              └         ┘
            >>> m = Matrix(((1, 2), ), shape=(2, 2), default=0)
            >>> print(m)
                0  1
              ┌      ┐
            0 │ 1  2 │
            1 │ 0  0 │
              └      ┘

    .. py:function:: Matrix(data: Sequence[T], shape: tuple[int, int], *, default: T) -> Matrix[T]

        Initialises a new :class:`Matrix` from a "flat" sequence.

        The *shape* and *default* arguments are both required, because neither
        of them can be inferred from *data*.

        The values from *data* will be read row-wise, and padded with *default*
        if they run out before the entire :class:`Matrix` is filled. Leftover
        values in *data* will simply be disregarded.

        :Example:

            >>> m = Matrix([1, 2, 3, 4, 5], shape=(2, 3), default=0)
            >>> print(m)
                0  1  2
              ┌         ┐
            0 │ 1  2  3 │
            1 │ 4  5  0 │
              └         ┘
            >>> m = Matrix(range(1, 100), shape=(2, 5), default=0)
            >>> print(m)
                0  1  2  3   4
              ┌                ┐
            0 │ 1  2  3  4   5 │
            1 │ 6  7  8  9  10 │
              └                ┘

    """

    # SHAPE MANIPULATION

    def transpose(self) -> Self:
        self._transpose()
        return self

    def resize(self, rows: int | tuple[int, int], cols: int | None = None) -> Self:
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

    def removerow(self, index: int) -> Self:
        self._removerow(index)
        return self

    def removecol(self, index: int) -> Self:
        self._removecol(index)
        return self

    def swaprows(self, a_index: int, b_index: int) -> Self:
        self._swaprows(a_index, b_index)
        return self

    def swapcols(self, a_index: int, b_index: int) -> Self:
        self._swapcols(a_index, b_index)
        return self

    # MATRIX OPERATIONS

    def imatadd(self, other: MatrixABC[V]) -> Self | Matrix[V]:
        """Add the matrix *other* in-situ.

        This behaves similar to :func:`matadd()`, but applies the result to
        the :class:`Matrix` instance itself.

        Equivalent to using the :code:`+=` operator with another
        :class:`MatrixT` as the right operand.

        :Example:

            >>> m = Matrix([[1, 1, 1], [2, 2, 2]], default=0)
            >>> m.imatadd(m)
            >>> print(m)
                0  1  2
              ┌         ┐
            0 │ 2  2  2 │
            1 │ 4  4  4 │
              └         ┘

        :param other: The :class:`MatrixT` instance whose cell values should be
            added to the cell values of this matrix.
        :returns: Its own :class:`Matrix` instance.
        """
        self._imatadd(other)
        return self

    def imatsub(self, other: MatrixABC[V]) -> Self | Matrix[V]:
        """Substitute the matrix *other* in-situ.

        This behaves similar to :func:`matsub()`, but applies the result to
        the :class:`Matrix` instance itself.

        Equivalent to using the :code:`-=` operator with another
        :class:`MatrixT` as the right operand.

        :Example:

            >>> m = Matrix([[1, 1, 1], [2, 2, 2]], default=0)
            >>> m.imatsub(m)
            >>> print(m)
                0  1  2
              ┌         ┐
            0 │ 0  0  0 │
            1 │ 0  0  0 │
              └         ┘

        :param other: The :class:`MatrixT` instance whose cell values should be
            subtracted from the cell values of this matrix.
        :returns: Its own :class:`Matrix` instance.
        """
        self._imatsub(other)
        return self

    def imatmul(self, other: MatrixABC[V]) -> Self | Matrix[V]:
        """Multiply with the matrix *other* in-situ.

        This behaves similar to :func:`matmul()`, but applies the result to
        the :class:`Matrix` instance itself.

        Note that this will alter the shape of the matrix.

        The matrix passed as *other* must have the inverse shape of the present
        matrix. E.g. if the instance has shape (2, 3), then the *other* matrix
        must have the shape (3, 2), otherwise the dot product is undefined and
        a `ValueError` will be raised.

        Equivalent to using the :code:`@=` operator with another
        :class:`MatrixT` as the right operand.

        :Example:

            >>> m = Matrix([[1, 1, 1], [2, 2, 2]], default=0)
            >>> n = Matrix([[1, 2], [1, 2], [1, 2]], default=0)
            >>> m.imatmul(m)
            >>> print(m)
                0   1
              ┌       ┐
            0 │ 3   6 │
            1 │ 6  12 │
              └       ┘

        :param other: The :class:`MatrixT` instance whose cell values should be
            added to the cell values of this matrix.
        :returns: Its own :class:`Matrix` instance.
        :raises ValueError: if the shape of *other* is not the inverse of this
            matrix instance itself.
        """
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

    # PROPERTIES

    @property
    def shape(self) -> tuple[int, int]:
        return self._shape

    @shape.setter
    def shape(self, shape: tuple[int, int]) -> None:
        self.resize(shape)

    @property
    def default(self) -> T:
        return self._default

    @default.setter
    def default(self, default: T) -> None:
        self._default = default

    # DATA GETTERS AND SETTERS

    @overload
    def set(
            self,
            _key: tuple[IndexT, IndexT],
            _values: T | Sequence[T] | Sequence[Sequence[T] | MatrixABC[T]],
            /,
            ) -> Self:
        ...

    @overload
    def set(
            self,
            _row: IndexT,
            _col: IndexT,
            _values: T | Sequence[T] | Sequence[Sequence[T] | MatrixABC[T]],
            /,
            ) -> Self:
        ...

    def set(
            self,
            arg1: IndexT | tuple[IndexT, IndexT],
            arg2: IndexT | T | Sequence[T] | Sequence[Sequence[T] | MatrixABC[T]] | Sentinel = NotGiven,
            arg3: T | Sequence[T] | Sequence[Sequence[T] | MatrixABC[T]] | Sentinel = NotGiven,
            /,
            ) -> Self:
        """
        (TO BE WRITTEN)
        """
        if arg3 is NotGiven:
            if not isinstance(arg1, Sequence):
                raise TypeError(
                    "Argument '_key' must be of type tuple[int | slice | tuple[int, ...], "
                    f"int | slice | tuple[int, ...]], not {type(arg1)}"
                )
            if len(arg1) != 2:
                raise ValueError(
                    "Argument '_key' must be exactly of length 2, got sequence of length "
                    f"{len(arg1)}"
                )
            if arg2 is NotGiven:
                raise TypeError("Missing required positional argument '_values'")
            row, col = arg1
            values = arg2
        else:
            if arg2 is NotGiven:
                raise TypeError("Missing required positional argument '_col'")
            if (not isinstance(arg1, (int, slice))
                and not (isinstance(arg1, tuple)
                         and len(arg1) > 0
                         and all(isinstance(i, int) for i in arg1))):
                raise TypeError(
                    "Argument '_row' must be of type int | slice | tuple[int, ...], "
                    f"not {type(arg1)}"
                )
            if (not isinstance(arg2, (int, slice))
                and not (isinstance(arg2, tuple)
                         and len(arg2) > 0
                         and all(isinstance(i, int) for i in arg2))):
                raise TypeError(
                    "Argument '_col' must be of type int | slice | tuple[int, ...], "
                    f"not {type(arg2)}"
                )
            if arg3 is NotGiven:
                raise TypeError("Missing required positional argument '_values'")
            row = arg1  # type: ignore # @FIXME
            col = arg2  # type: ignore # @FIXME
            values = arg3
        if not isinstance(row, (slice, int, tuple)) or not isinstance(col, (slice, int, tuple)):
            raise TypeError(
                "Matrix indices must be tuples of type (int | slice | tuple[int, ...], int | slice "
                f"| tuple[int, ...]), not ({type(row)}, {type(col)})"
            )
        if isinstance(row, (slice, tuple)) or isinstance(col, (slice, tuple)):
            if not isinstance(values, (Sequence, MatrixABC)):
                raise TypeError(
                    "Values passed for matrix slice assignment must be of type Sequence or "
                    f"MatrixABC, not {type(values)}"
                )
            values_ = cast(Sequence[T] | Sequence[Sequence[T]] | MatrixABC[T], values)
            self._setslice(row, col, values_)
        else:
            value_ = cast(T, values)
            self._setitem(row, col, value_)
        return self

    def __setitem__(self, key: tuple[IndexT, IndexT], value: T | Sequence[T] | Sequence[Sequence[T] | MatrixABC[T]]) -> None:
        self.set(key, value)

    def __delitem__(self, key: tuple[IndexT, IndexT]) -> None:
        self.__setitem__(key, self._default)

    # DUNDER METHODS

    def __iadd__(self, other: MatrixABC[V] | V) -> Self | Matrix[V]:
        if isinstance(other, MatrixABC):
            return self.imatadd(other)
        return self.iscaladd(other)

    def __isub__(self, other: MatrixABC[V] | V) -> Self | Matrix[V]:
        if isinstance(other, MatrixABC):
            return self.imatsub(other)
        return self.iscalsub(other)

    def __imul__(self, other: V) -> Self | Matrix[V]:
        return self.iscalmul(other)

    def __imatmul__(self, other: MatrixABC[V]) -> Self | Matrix[V]:
        return self.imatmul(other)
