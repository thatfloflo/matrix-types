"""Base class for Matrix types."""
from __future__ import annotations
from abc import ABC, abstractmethod
from copy import deepcopy
from itertools import chain
from typing import Any, Callable, Generic, Self, Iterator, Sequence, Sized, overload, cast
from ._types import T, V, RowColT, IndexT
from ._iterutils import chunked, matmul
from .formatter import DefaultFormatter


copyfunc = deepcopy


class MatrixABC(ABC, Generic[T]):
    """Abstract base class for 2-dimensional matrix types."""

    _data: list[list[T]]
    _default: T
    _shape: tuple[int, int] = (0, 0)

    _rowrange: range
    _colrange: range

    @overload
    def __init__(self, data: Sequence[Sequence[T]], *, default: T):
        ...

    @overload
    def __init__(self, data: Sequence[Sequence[T]], shape: tuple[int, int], *, default: T):
        ...

    @overload
    def __init__(self, data: MatrixABC[T]):
        ...

    @overload
    def __init__(self, data: MatrixABC[T], *, default: T):
        ...

    @overload
    def __init__(self, data: MatrixABC[T], shape: tuple[int, int]):
        ...

    @overload
    def __init__(self, data: MatrixABC[T], shape: tuple[int, int], *, default: T):
        ...

    @overload
    def __init__(self, data: Sequence[T], shape: tuple[int, int], *, default: T):
        ...

    def __init__(self, *args: Any, **kwargs: Any):  # noqa: C901
        """Initialise a new Matrix/FrozenMatrix instance.

        :param MatrixABC[T] | Sequence[T] | Sequence[Sequence[T]] data: The
            initial data for the matrix. This can be another `MatrixT` instance,
            a sequence of values, or a sequence of a sequence of values.
            This argument is required, but you can simply pass an empty sequence
            (e.g. :code:`[]`) to have the matrix filled with *default* instead.
        :param tuple[int, int] shape: The shape the matrix should have, as a
            tuple specifying :code:`(rows, cols)`. This argument is required if
            *data* is a flat sequence. If *data* is a sequence of sequences or
            another `MatrixT`, then *shape* will be inferred if it is not
            provided, or *data* will be reshaped to *shape* if it is provided
            and doesn't presently conform to *shape*.
        :param T default: A keyword-only argument specifying the default value
            for matrix cells. This will be used to fill in the value for cells
            which do not have one assigned, are deleted, newly inserted, etc.
            It is also used as in evaluating the truthiness of a `MatrixT` (a
            `MatrixT` is :code:`True` if at least one of its cells' values is
            **not** equal to *default*). The *default* argument is required
            unless *data* is of type `MatrixT`, in which case it will be
            inferred if not explicity specified.
        """
        # Make args/kwargs uniform (data, shape, default=default)
        arglist = list(args)
        if "data" in kwargs:
            arglist.insert(0, kwargs["data"])
            del kwargs["data"]
        if "shape" in kwargs:
            arglist.insert(1, kwargs["shape"])
            del kwargs["shape"]
        if "default" not in kwargs and isinstance(arglist[0], MatrixABC):
            kwargs["default"] = arglist[0]._default
        if len(arglist) < 1:
            raise TypeError("Expected at least 1 argument, 0 given")
        if len(arglist) > 2:
            raise TypeError("Unexpected argument, expected at most 2 non-keyword arguments")
        # Extract values for data, shape and default
        data = arglist[0]
        if len(arglist) < 2:
            if isinstance(data, MatrixABC):
                shape = data._shape
            elif isinstance(data, Sequence) and len(data) == 0:
                shape = (0, 0)
            elif isinstance(data, Sequence) and all(isinstance(x, Sequence) for x in data):
                shape = (len(data), max(len(x) for x in data))
            else:
                raise TypeError("Missing required argument 'shape'")
        else:
            shape = arglist[1]
        if "default" in kwargs:
            default = kwargs["default"]
            del kwargs["default"]
        else:
            if isinstance(data, MatrixABC):
                default = data._default
            else:
                raise TypeError("Missing required argument 'default'")
        if len(kwargs) > 0:
            raise TypeError(
                f"Unexpected keyword argument(s): {', '.join(repr(k) for k in kwargs.keys())}"
            )
        # Check types for data, shape and default
        if not isinstance(data, (MatrixABC, Sequence)):
            raise TypeError(
                f"Argument 'data' must be of type Matrix or Sequence, not {type(data)}"
            )
        if (not isinstance(shape, tuple)
                or len(shape) != 2
                or not isinstance(shape[0], int)
                or not isinstance(shape[1], int)):
            _desc = (f"{type(shape)} of length {len(shape)}"
                     if isinstance(shape, Sized)
                     else type(shape))
            raise TypeError(f"Argument 'shape' must be of type tuple[int, int], not {_desc}")
        # Make sure we do not have negative shape values
        self._check_shape(shape)
        # Initialise matrix
        if isinstance(data, MatrixABC):
            self._init_from_matrix(data, shape, default)
        if isinstance(data, Sequence):
            if len(data) > 0 and all(isinstance(x, Sequence) for x in data):
                self._init_from_seqseq(data, shape, default)
            else:
                self._init_from_sequence(data, shape, default)
        # Calculate helpers
        self._calculate_helpers()
        # Do any reshaping if needed
        if self._shape != shape:
            self._resize(shape)

    def _init_from_matrix(self, data: MatrixABC[T], shape: tuple[int, int], default: T) -> None:
        """Initialise Matrix from another Matrix."""
        self._data = copyfunc(data._data)
        self._shape = copyfunc(data._shape)
        self._default = copyfunc(data._default)

    def _init_from_seqseq(
            self,
            data: Sequence[Sequence[T]],
            shape: tuple[int, int],
            default: T) -> None:
        """Initialise Matrix from another Matrix."""
        self._default = default
        self._shape = shape
        self._data = []
        data = list(data)
        if len(data) < self._shape[0]:
            for _ in range(len(data), self._shape[0]):
                data.append([self._default] * self._shape[1])
        for row in data[0:self._shape[0]]:
            if len(row) < self._shape[1]:
                self._data.append(
                    list(row) + [self._default] * (self._shape[1] - len(row))
                )
            else:
                self._data.append(list(row)[0:self._shape[1]])

    def _init_from_sequence(self, data: Sequence[T], shape: tuple[int, int], default: T) -> None:
        """Initialise Matrix from another Matrix."""
        self._default = default
        self._shape = shape
        number_of_cells = self._shape[0] * self._shape[1]
        raw_seq = list(data)
        if len(raw_seq) < number_of_cells:
            raw_seq.extend([self._default] * (number_of_cells - len(raw_seq)))
        x = raw_seq[0:number_of_cells]
        self._data = list(chunked(x, self._shape[1]))

    # HELPER FUNCTIONS

    def _calculate_helpers(self) -> None:
        """Calculates several useful helpers.

        .. important::

            You must call _calculate_helpers() after every internal operation
            which alters the shape of the matrix. This is because internals
            such as `self._rowrange` and `self._colrange` must be recalculated
            after such operations or the ranges won't match the shape of the
            matrix.
        """
        self._rowrange = range(0, self._shape[0])
        self._colrange = range(0, self._shape[1])

    def _check_shape(self, shape: tuple[int, int]) -> None:
        """Checks whether a shape tuple is valid in terms of values."""
        if shape[0] < 0:
            raise ValueError("Row count cannot be negative")
        if shape[1] < 0:
            raise ValueError("Column count cannot be negative")

    def _check_rowindex(self, row: IndexT) -> None:
        """Checks whether a row index is in range or out of range.

        :param row: The row index to check.
        :raises IndexError: if the row index is out of range.
        """
        if not isinstance(row, (int, tuple, slice)):
            raise TypeError(
                f"Row index must be of type int | slice | tuple[int, ...], not {type(row)!r}"
            )
        if isinstance(row, int) and (row == self._shape[0] or abs(row) > self._shape[0]):
            raise IndexError("Row index out of range")
        if isinstance(row, tuple):
            if not all(isinstance(x, int) for x in row):
                raise TypeError("Row index tuple must only contain integer indices")
            if any(x == self._shape[0] or abs(x) > self._shape[0] for x in row):
                raise IndexError("At least one row index out of range in index tuple")

    def _check_colindex(self, col: IndexT) -> None:
        """Checks whether a column index is in range or out of range.

        :param col: The column index to check.
        :raises IndexError: if the column index is out of range.
        """
        if not isinstance(col, (int, tuple, slice)):
            raise TypeError(
                "Column index must be of type int | slice | tuple[int, ...], "
                f"not {type(col)!r} given"
            )
        if isinstance(col, int) and (col == self._shape[1] or abs(col) > self._shape[1]):
            raise IndexError("Column index out of range")
        if isinstance(col, tuple):
            if not all(isinstance(x, int) for x in col):
                raise TypeError("Column index tuple must only contain integer indices")
            if any(x == self._shape[1] or abs(x) > self._shape[1] for x in col):
                raise IndexError("At least one column index out of range in index tuple")

    def _rowtoindices(self, index: IndexT) -> tuple[int, ...]:
        """Converts an integer or a slice to a tuple of row indices.

        :param intorslice: An integer or `slice` object referring to one or
            more row indices.
        :returns: a tuple of integers with the indices of all the rows within
            range specified by *intorslice*.
        """
        if isinstance(index, int):
            self._check_rowindex(index)
            return (index,)
        if isinstance(index, tuple):
            self._check_rowindex(index)
            return index
        start = index.start or 0
        if start < 0:
            start = max(self._shape[0] - abs(start), 0)
        stop = index.stop or self._shape[0]
        if stop < 0:
            stop = max(self._shape[0] - abs(stop), 0)
        return tuple(range(
            start,
            stop,
            index.step or 1
        ))

    def _coltoindices(self, index: IndexT) -> tuple[int, ...]:
        """Converts an integer or a slice to a tuple of column indices.

        :param intorslice: An integer or `slice` object referring to one or
            more column indices.
        :returns: a tuple of integers with the indices of all the columns
            within range specified by *intorslice*.
        """
        if isinstance(index, int):
            self._check_colindex(index)
            return (index,)
        if isinstance(index, tuple):
            self._check_colindex(index)
            return index
        start = index.start or 0
        if start < 0:
            start = max(self._shape[1] - abs(start), 0)
        stop = index.stop or self._shape[1]
        if stop < 0:
            stop = max(self._shape[1] - abs(stop), 0)
        return tuple(range(
            start,
            stop,
            index.step or 1
        ))

    # PROPERTIES

    @property
    def shape(self) -> tuple[int, int]:
        """Returns the shape of the matrix."""
        return self._shape

    @property
    def default(self) -> T:
        """Returns the *default* value for the matrix."""
        return self._default

    def empty(self) -> bool:
        """Returns :code:`False` if at least one value in the """
        if 0 in self._shape:
            return True
        return all(
            self._data[r][c] == self._default for c in self._colrange for r in self._rowrange
        )

    # SHAPE MANIPULATION

    def _transpose(self) -> None:
        """Transposes the rows and columns of the internal data."""
        self._data = [list(row) for row in zip(*self._data, strict=True)]
        self._shape = (self._shape[1], self._shape[0])
        self._calculate_helpers()

    @abstractmethod
    def transpose(self) -> Self:
        """Transposes the rows and columns of the matrix.

        This has the effect of turning a matrix such as::

                0  1  2
              ┌         ┐
            0 │ 1  2  3 │
            1 │ 4  5  6 │
              └         ┘

        into the matrix::

                0  1
              ┌      ┐
            0 │ 1  4 │
            1 │ 2  5 │
            2 │ 3  6 │
              └      ┘

        Modifies the matrix in-situ if it is mutable, otherwise returns a
        transposed copy of the matrix.

        :returns: its own :class:`Matrix` instance if mutable,
            a copy of the :class:`FrozenMatrix` instance if immutable.
        """
        raise NotImplementedError()

    def _resize(self, rows: int | tuple[int, int], cols: int | None = None) -> None:
        """Resizes the internal data to the specified shape, with origin (0, 0)."""
        if cols is None and isinstance(rows, Sequence) and len(rows) == 2:
            rows = cast(tuple[int, int], rows)  # For whatever reason mypy thinks rows is <nothing>
            cols = rows[1]
            rows = rows[0]
        elif not isinstance(rows, int) or not isinstance(cols, int):
            raise ValueError(
                "Arguments 'rows' and 'cols' must both be of type 'int', "
                f"not {type(rows)} and {type(cols)}"
            )
        self._check_shape((rows, cols))
        if rows > self._shape[0]:
            rows_to_add = rows - self._shape[0]
            for _ in range(0, rows_to_add):
                self._data.append([self._default] * self._shape[1])
        elif rows < self._shape[0]:
            del self._data[rows:]
        if cols > self._shape[1]:
            cols_to_add = cols - self._shape[1]
            for row in range(0, rows):
                self._data[row] += [self._default] * cols_to_add
        elif cols < self._shape[1]:
            for row in range(0, rows):
                del self._data[row][cols:]
        self._shape = (rows, cols)
        self._calculate_helpers()

    @overload
    @abstractmethod
    def resize(self, rows_or_shape: tuple[int, int]) -> Self:
        ...

    @overload
    @abstractmethod
    def resize(self, rows_or_shape: int, cols: int) -> Self:
        ...

    @abstractmethod
    def resize(self, rows_or_shape: int | tuple[int, int], cols: int | None = None) -> Self:
        """Grows or shrinks a matrix.

        Grows or shrinks a matrix depending on whether the new shape supplied
        is greater or smaller in any dimension; does nothing if the new shape
        is identical to the original shape.

        Where the new shape adds new rows or columns, the new cells are
        populated by the matrix's default value.

        Where the new shape removes rows or columns, the values of the removed
        cells will be lost.

        Modifies the matrix in-situ if it is mutable, otherwise returns a
        resized copy of the matrix.

        Can be called either with the positional-only argument *shape* as

        .. py:function:: resize(shape: tuple[int, int]) -> Self

        or with two integer arguments for *rows* and *cols* as

        .. py:function:: resize(rows: int, cols: int) -> Self

        :param tuple[int, int] shape: A tuple with the sizes for (rows, columns)
            that the resized matrix should have.
        :param rows: The number of rows the resized matrix should have.
        :param cols: The number of columns the resized matrix should have.
        :returns: its own :class:`Matrix` instance or a copy of the :class:`FrozenMatrix` instance.
        """
        raise NotImplementedError()

    def _flip(self, *, by: RowColT = "row") -> None:
        """Flips the internal data vertically or horizontally."""
        if by == "row":
            self._data.reverse()
            return
        if by == "col":
            for row in self._rowrange:
                self._data[row].reverse()
            return
        raise ValueError(f"Unknown value '{by}' for argument 'by', must be 'row' or 'col'")

    @abstractmethod
    def flip(self, *, by: RowColT = "row") -> Self:
        """Flips a matrix vertically or horizontally.

        Effectively reverses the order of the matrix's rows or columns.

        Whether the flipping is applied to the rows or columns is specified
        by the keyword-only argument *by*. The default is :code:`"row"`,
        which flips the matrix vertically.

        :code:`m.flip()` and :code:`m.flip(by="row")` are equivalent to
        :code:`m.flipv()`.

        :code:`m.flip(by="column")` is equivalent to :code:`m.fliph()`.

        :param by: Whether to flop row-wise or column-wise, must be one of the
            literal strings :code:`"row"` (the default) or :code:`"col"`.
        :returns: its own :class:`Matrix` instance if mutable,
            a copy of the :class:`FrozenMatrix` instance if immutable.
        """
        raise NotImplementedError()

    def fliph(self) -> Self:
        """Flips a matrix horizontally (by columns).

        This effectively reverses the order of the columns of the matrix.

        This has the effect of turning a matrix such as::

                0  1  2
              ┌         ┐
            0 │ 1  2  3 │
            1 │ 4  5  6 │
              └         ┘

        into the matrix::

                0  1  2
              ┌         ┐
            0 │ 3  2  1 │
            1 │ 6  5  4 │
              └         ┘

        Modifies the matrix in-situ if the matrix is mutable, otherwise returns
        a copy of the matrix with the order of columns reversed.

        :returns: its own :class:`Matrix` instance if mutable,
            a copy of the :class:`FrozenMatrix` instance if immutable.
        """
        return self.flip(by="col")

    def flipv(self) -> Self:
        """Flips a matrix vertically (by rows).

        This effectively reverses the order of the rows of the matrix.

        This has the effect of turning a matrix such as::

                0  1  2
              ┌         ┐
            0 │ 1  2  3 │
            1 │ 4  5  6 │
            2 │ 7  8  9 │
              └         ┘

        into the matrix::

                0  1  2
              ┌         ┐
            0 │ 7  8  9 │
            1 │ 4  5  6 │
            2 │ 1  2  3 │
              └         ┘

        Modifies the matrix in-situ if the matrix is mutable, otherwise returns
        a copy of the matrix with the order of rows reversed.

        :returns: its own :class:`Matrix` instance if mutable,
            a copy of the :class:`FrozenMatrix` instance if immutable.
        """
        return self.flip(by="row")

    def _insertrow(self, index: int, data: Sequence[T]) -> None:
        """Inserts a new row into the internal data."""
        data = list(data)
        # Ensure data's length is correct
        if len(data) > self._shape[1]:
            del data[self._shape[1]:]
        elif len(data) < self._shape[1]:
            data += [self._default] * (self._shape[1] - len(data))
        # Insert new data at index
        self._data.insert(index, data)
        self._shape = (self._shape[0] + 1, self._shape[1])
        self._calculate_helpers()

    @abstractmethod
    def insertrow(self, index: int, data: Sequence[T]) -> Self:
        """Inserts a row with values *data* before *index*.

        *data* must be a sequence with length at least matching the number of
        columns in the matrix. Unused values will be ignored.

        Modifies the matrix in-situ if the matrix is mutable, otherwise returns
        an expanded copy of the matrix.

        :param index: The row index before which the new row should be inserted.
        :param data: The data to be inserted into the new row.
        :returns: its own :class:`Matrix` instance or a copy of the :class:`FrozenMatrix` instance.
        """
        raise NotImplementedError()

    def _insertcol(self, index: int, data: Sequence[T]) -> None:
        """Inserts a new column into the internal data."""
        data = list(data)
        # Ensure data's length is correct
        if len(data) > self._shape[0]:
            del data[self._shape[0]:]
        elif len(data) < self._shape[0]:
            data += [self._default] * (self._shape[0] - len(data))
        # Insert new data at index
        for row in self._rowrange:
            self._data[row].insert(index, data[row])
        self._shape = (self._shape[0], self._shape[1] + 1)
        self._calculate_helpers()

    @abstractmethod
    def insertcol(self, index: int, data: Sequence[T]) -> Self:
        """Inserts a column with values *data* before *index*.

        *data* must be a sequence with length at least matching the number of
        rows in the matrix. Unused values will be ignored.

        Modifies the matrix in-situ if the matrix is mutable, otherwise returns
        an expanded copy of the matrix.

        :param index: The colmn index before which the new column should be inserted.
        :param data: The data to be inserted into the new column.
        :returns: its own :class:`Matrix` instance or a copy of the :class:`FrozenMatrix` instance.
        """
        raise NotImplementedError()

    def appendrow(self, data: Sequence[T]) -> Self:
        """Appends a row with values *data* at the bottom of the matrix.

        This is equivalent to :code:`m.insertrow(len(m), data)`.

        *data* must be a sequence with length at least matching the number of
        columns in the matrix. Unused values will be ignored.

        Modifies the matrix in-situ and returns *self* if the matrix is
        mutable, otherwise returns an expanded copy of the matrix.

        :param data: The data to be inserted into the new row.
        :returns: its own :class:`Matrix` instance if mutable,
            a copy of the :class:`FrozenMatrix` instance if immutable.
        """
        return self.insertrow(self._shape[0], data)

    def appendcol(self, data: Sequence[T]) -> Self:
        """Appends a column with values *data* to the right of the matrix.

        This is equivalent to :code:`m.insertcol(len(m), data)`.

        *data* must be a sequence with length at least matching the number of
        rows in the matrix. Unused values will be ignored.

        Modifies the matrix in-situ and returns *self* if the matrix is
        mutable, otherwise returns an expanded copy of the matrix.

        :param data: The data to be inserted into the new column.
        :returns: its own :class:`Matrix` instance if mutable,
            a copy of the :class:`FrozenMatrix` instance if immutable.
        """
        return self.insertcol(self._shape[1], data)

    def prependrow(self, data: Sequence[T]) -> Self:
        """Prepends a row with values *data* at the bottom of the matrix.

        This is equivalent to :code:`m.insertrow(0, data)`.

        *data* must be a sequence with length at least matching the number of
        rows in the matrix. Unused values will be ignored.

        Modifies the matrix in-situ if the matrix is mutable, otherwise returns
        an expanded copy of the matrix.

        :param data: The data to be inserted into the new row.
        :returns: its own :class:`Matrix` instance or a copy of the :class:`FrozenMatrix` instance.
        """
        return self.insertrow(0, data)

    def prependcol(self, data: Sequence[T]) -> Self:
        """Prepends a column with values *data* to the right of the matrix.

        This is equivalent to :code:`m.insertcol(0, data)`.

        *data* must be a sequence with length at least matching the number of
        columns in the matrix. Unused values will be ignored.

        Modifies the matrix in-situ if the matrix is mutable, otherwise returns
        an expanded copy of the matrix.

        :param data: The data to be inserted into the new column.
        :returns: its own :class:`Matrix` instance or a copy of the :class:`FrozenMatrix` instance.
        """
        return self.insertcol(0, data)

    def _removerow(self, index: int) -> None:
        """Removes a row from the internal data."""
        self._check_rowindex(index)
        del self._data[index]
        self._shape = (self._shape[0] - 1, self._shape[1])
        self._calculate_helpers()

    @abstractmethod
    def removerow(self, index: int) -> Self:
        """Removes the row at *index*.

        .. caution::
            The row is *removed completely* from the matrix, and
            the matrix's shape will be altered. Calling this function
            *does not* merely reset the values of items in the targeted
            row to their default!

        :param index: The index of the row to be removed.
        :returns: its own :class:`Matrix` instance if mutable,
            a copy of the :class:`FrozenMatrix` instance if immutable.
        """
        raise NotImplementedError()

    def _removecol(self, index: int) -> None:
        """Removes a column from the internal data."""
        for row in self._rowrange:
            del self._data[row][index]
        self._shape = (self._shape[0], self._shape[1] - 1)
        self._calculate_helpers()

    @abstractmethod
    def removecol(self, index: int) -> Self:
        """Remove the column at *index*.

        .. caution::
            The column is *removed completely* from the matrix, and
            the matrix's shape will be altered. Calling this function
            *does not* merely reset the values of items in the targeted
            column to their default!

        :param index: The index of the column to be removed.
        :returns: its own :class:`Matrix` instance if mutable,
            a copy of the :class:`FrozenMatrix` instance if immutable.
        """
        raise NotImplementedError()

    def _swaprows(self, a_index: int, b_index: int) -> None:
        """Swaps two rows in the internal data."""
        self._check_rowindex(a_index)
        self._check_rowindex(b_index)
        self._data[a_index], self._data[b_index] = self._data[b_index], self._data[a_index]

    @abstractmethod
    def swaprows(self, a_index: int, b_index: int) -> Self:
        """Swaps the two rows at indices *a_index* and *b_index*.

        Modifies the matrix in-situ if the matrix is mutable, otherwise returns
        a copy with the two rows swapped.

        :param a_index: The index of the first row to be swapped.
        :param b_index: The index of the second row, which *a_index* should be swapped with.
        :returns: its own :class:`Matrix` instance or a copy of the :class:`FrozenMatrix` instance.
        """
        raise NotImplementedError()

    def _swapcols(self, a_index: int, b_index: int) -> None:
        """Swaps two columns in the internal data."""
        self._check_colindex(a_index)
        self._check_colindex(b_index)
        for row in self._rowrange:
            self._data[row][a_index], self._data[row][b_index] = \
                self._data[row][b_index], self._data[row][a_index]

    @abstractmethod
    def swapcols(self, a_index: int, b_index: int) -> Self:
        """Swaps the two columns at indices *a_index* and *b_index*.

        Modifies the matrix in-situ if the matrix is mutable, otherwise returns
        a copy with the two columns swapped.

        :param a_index: The index of the first column to be swapped.
        :param b_index: The index of the second column, which *a_index* should be swapped with.
        :returns: its own :class:`Matrix` instance or a copy of the :class:`FrozenMatrix` instance.
        """
        raise NotImplementedError()

    # MATRIX OPERATIONS

    def _imatadd(self, other: MatrixABC[Any]) -> None:
        """Internally adds the values of *other* Matrix to this one."""
        # Check shapes are compatible
        if self._shape != other._shape:
            raise ValueError(f"Matrices don't match in shape: {self._shape} + {other._shape}")
        for row in self._rowrange:
            for col in self._colrange:
                self._data[row][col] = self._data[row][col] + other._data[row][col]

    def matadd(self, other: MatrixABC[V]) -> Self | MatrixABC[V]:
        """Adds two matrices.

        The *other* matrix must have the same shape as the matrix to which
        it is added.

        Returns a new matrix of the same shape as the original matrix.

        :param other: The :class:`Matrix` or :class:`FrozenMatrix` to be
            added to this one.
        :returns: a copy of the :class:`Matrix` or :class:`FrozenMatrix`
            instance with *other* added.
        """
        new = self.copy()
        new._imatadd(other)
        return new

    def _imatsub(self, other: MatrixABC[Any]) -> None:
        """Internally subtracts the values of *other* Matrix from this one."""
        # Check shapes are compatible
        if self._shape != other._shape:
            raise ValueError(f"Matrices don't match in shape: {self._shape} @ {other._shape}")
        for row in self._rowrange:
            for col in self._colrange:
                self._data[row][col] = self._data[row][col] - other._data[row][col]

    def matsub(self, other: MatrixABC[V]) -> Self | MatrixABC[V]:
        """Subtracts two matrices.

        The *other* matrix must have the same shape as the matrix from which
        it is subtracted.

        Returns a new matrix of the same shape as the original matrix.

        :param other: The :class:`Matrix` or :class:`FrozenMatrix` to be
            subtracted from this one.
        :returns: a copy of the :class:`Matrix` or :class:`FrozenMatrix`
            instance with *other* subtracted.
        """
        new = self.copy()
        new._imatsub(other)
        return new

    def _imatmul(self, other: MatrixABC[Any]) -> None:
        """Matrix-multiplies internal data with *other* matrix."""
        if self._shape != (other._shape[1], other._shape[0]):
            raise ValueError("Shape of *other* matrix not compatible for matrix multiplication")
        self._data = list(matmul(self._data, other._data))
        self._shape = (self._shape[0], other._shape[1])
        self._calculate_helpers()

    def matmul(self, other: MatrixABC[V]) -> Self | MatrixABC[V]:
        """Multiplies two matrices.

        The *other* matrix's shape must be the inverse of the matrix to which
        it applies. For example, if we have a matrix of shape (2, 3), it can
        only be multiplied with a matrix of the shape (3, 2).

        Returns a new matrix of shape (k, n), where *k* is the number of rows
        of the original matrix and *n* is the number of columns of the *other*
        matrix.

        :param other: The :class:`Matrix` or :class:`FrozenMatrix` to be
            multiplied with this one.
        :returns: a copy of the :class:`Matrix` or :class:`FrozenMatrix`
            instance with *other* multiplied into it.
        """
        new = self.copy()
        new._imatmul(other)
        return new

    def _iscaladd(self, scalar: Any) -> None:
        """Internally add the scalar *scalar* to all values."""
        for row in self._rowrange:
            for col in self._colrange:
                self._data[row][col] = self._data[row][col] + scalar

    def scaladd(self, scalar: V) -> Self | MatrixABC[V]:
        """Adds *scalar* to the value of each cell in the matrix.

        Returns a copy of the matrix with the scalar addition applied.

        :param scalar: The scalar to be added to each cell's value.
        :returns: a copy of the :class:`Matrix` or :class:`FrozenMatrix`
            instance with *scalar* added to its cell values.
        """
        new = self.copy()
        new._iscaladd(scalar)
        return new

    def _iscalsub(self, scalar: Any) -> None:
        for row in self._rowrange:
            for col in self._colrange:
                self._data[row][col] = self._data[row][col] - scalar

    def scalsub(self, scalar: V) -> Self | MatrixABC[V]:
        """Subtracts *scalar* from the value of each cell in the matrix.

        Returns a copy of the matrix with the scalar subtraction applied.

        :param scalar: The scalar to be subtracted from each cell's value.
        :returns: a copy of the :class:`Matrix` or :class:`FrozenMatrix`
            instance with *scalar* subtracted from its cell values.
        """
        new = self.copy()
        new._iscalsub(scalar)
        return new

    def _iscalmul(self, scalar: Any) -> None:
        """Internally multiplies each cell value with *scalar*."""
        for row in self._rowrange:
            for col in self._colrange:
                self._data[row][col] = self._data[row][col] * scalar

    def scalmul(self, scalar: V) -> Self | MatrixABC[V]:
        """Multiplies the value of each cell in the matrix with *scalar*.

        Returns a copy of the matrix with the scalar multiplication applied.

        :param scalar: The scalar to be subtracted from each cell's value.
        :returns: a copy of the :class:`Matrix` or :class:`FrozenMatrix`
            instance with *scalar* multiplied into each cell's values.
        """
        new = self.copy()
        new._iscalmul(scalar)
        return new

    def _foreach(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """Internally applies *func* to each cell."""
        for row in self._rowrange:
            for col in self._colrange:
                func(self._data[row][col], *args, **kwargs)

    def foreach(
        self,
        func: Callable[..., V],
        *args: Any,
        **kwargs: Any
    ) -> Self | MatrixABC[V]:
        """Applies *func* to each cell in the matrix.

        Any additional *args* or *kwargs* passed after *func* will be passed
        as arguments to *func*.

        The return value of *func* will be ignored. To mutate the values
        of each cell in-situ based on the return value, use :func:`map()`
        instead.

        :Example:

            >>> print(m)
            ┌         ┐
            │ 1  2  3 │
            │ 4  5  6 │
            └         ┘
            >>> m.foreach(lambda a: print(a**2, end=", "))
            1, 4, 9, 16, 25, 36,

        :param func: A callable accepting at least one argument (namely the
            value of each cell as the matrix is being iterated over).
        :returns: its own :class:`Matrix` instance or a copy of the
            :class:`FrozenMatrix` instance.
        """
        self._foreach(func, *args, **kwargs)
        return self

    def _map(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """Internally applies *func* to each cell and stores the return value in cell."""
        for row in self._rowrange:
            for col in self._colrange:
                self._data[row][col] = func(self._data[row][col], *args, **kwargs)

    @abstractmethod
    def map(
        self,
        func: Callable[..., V],
        *args: Any,
        **kwargs: Any
    ) -> Self | MatrixABC[V]:
        """Applies *func* to each cell in the matrix and stores the return value
        of *func* as the new cell value.

        Any additional *args* or *kwargs* passed after *func* will be passed
        as parameters to *func*.

        This will mutate the values of each cell in-situ based on the return
        value of *func*. To apply *func* without affecting the values store
        in the matrix, use :func:`foreach()` instead.

        Returns the original matrix with *func* applied in-situ if the matrix
        is mutable, otherwise returns a copy of the matrix with *func* applied.

        :Example:

            >>> m = Matrix([[1, 2, 3], [4, 5, 6]], default=0)
            >>> print(m)
                0  1  2
              ┌         ┐
            0 │ 1  2  3 │
            1 │ 4  5  6 │
              └         ┘
            >>> print(m.map(lambda a: a**2))
                 0   1   2
              ┌            ┐
            0 │  1   4   9 │
            1 │ 16  25  36 │
              └            ┘

        :param func: A callable accepting at least one argument (namely the
            value of each cell as the matrix is being iterated over).
        :param args: Additional positional arguments to be passed to *func*.
        :param kwargs: Additional keyword arguments to be passed to *func*.
        :returns: its own :class:`Matrix` instance if mutable,
            a copy of the :class:`FrozenMatrix` instance if immutable.
        """
        raise NotImplementedError()

    # DATA ACCESS MODALITIES

    def copy(self) -> Self:
        """Returns a copy of the matrix object.

        :returns: A copy of *self*.
        """
        return copyfunc(self)

    def aslist(self, *, by: RowColT = "row") -> list[list[T]]:
        """Returns the matrix data as a list of lists.

        If *by* is :code:`"row"` (the default), then the returned list of lists
        is in the format *rows[columns]*. If *by* is :code:`"col"` then the
        returned list is in the format *columns[rows]*.

        For example, the matrix::

                 0  1  2
               ┌         ┐
            0  │ 1  2  3 │
            1  │ 4  5  6 │
               └         ┘

        will be returned as a list of the form::

            [
                [1, 2, 3],
                [4, 5, 6]
            ]

        Note that this is different from invoking :code:`list(m)` on a matrix,
        which does not return a list of list with the matrix's values, but
        rather a list of :code:`(row, col)` index pairs for each cell,
        equivalent to calling :func:`keys()` on a matrix object.

        :param by: Specifies whether to build the list row-wise or column-wise.
        :returns: A list containing one list for each row/column, depending on
            the direction indicated by the *by* argument.
        """
        if by == "row":
            return [list(row) for row in self._data]  # Ensure shallow copy of rows
        elif by == "col":
            return [list(row) for row in zip(*self._data, strict=True)]
        raise TypeError("Argument 'by' must be literal 'row' or 'col'")

    def asdict(self) -> dict[tuple[int, int], T]:
        """Returns the matrix data as a dictionary with coordinates as key.

        The returned dictionary's keys are tuples of the form
        :code:`(row, column)`.

        For example, the matrix::

                 0  1  2
               ┌         ┐
            0  │ 1  2  3 │
            1  │ 4  5  6 │
               └         ┘

        will be returned as a dict of the form::

            {
                (0, 0): 1,
                (0, 1): 2,
                (0, 2): 3,
                (1, 0): 4,
                (1, 1): 5,
                (1, 2): 6
            }

        :returns: A dictionary with coordinates as keys and cell values as
            values.
        """
        return {(r, c): self._data[r][c] for r in self._rowrange for c in self._colrange}

    def keys(self, *, by: RowColT = "row") -> list[tuple[int, int]]:
        """Returns a list of keys for all cells in the matrix.

        The list contains tuples with the coordinates in the form
        :code:`(row, col)`. These are sorted by row first if *by* is set to
        :code:`"row"` (the default), and they are sorted by column first if
        *by* is set to :code:`"col"`.

        :param by: Whether to sort the keys row-wise or column-wise.
        :returns: A list of tuples with coordinates for each cell, sorted as
            indicated by the *by* argument.
        """
        if by == "row":
            return [(r, c) for r in self._rowrange for c in self._colrange]
        elif by == "col":
            return [(r, c) for c in self._colrange for r in self._rowrange]
        raise TypeError("Argument 'by' must be literal 'row' or 'col'")

    def values(self, *, by: RowColT = "row") -> list[T]:
        """Returns a flat list of the matrix's values.

        By default, the returned list will be sequenced row by row.
        For example, the matrix::
                0  1  2
              ┌         ┐
            0 │ 1  2  3 │
            1 │ 4  5  6 │
              └         ┘

        will be returned as the list::

            [1, 2, 3, 4, 5, 6]

        This behaviour can be modified by passing the literal `"column"` as the
        keyword-only argument *by*, such that :code:`m.values(by="column")`
        would return::

            [1, 4, 2, 5, 3, 6]

        :param by: The direction in which the matrix values should be
            serialised into a flat sequence, row-wise or column-wise.
        :returns: A list with the matrix's values.
        """
        if by == "row":
            return list(chain(*self._data))
        elif by == "col":
            transposed = (list(row) for row in zip(*self._data, strict=True))
            return list(chain(*transposed))
        raise TypeError("Argument 'by' must be literal 'row' or 'col'")

    def items(self, *, by: RowColT = "row") -> list[tuple[tuple[int, int], T]]:
        """Returns a list of key--value pairs for all cells in the matrix.

        Each item in the returned list is a tuple of the form
        :code:`((row, col), value)`.

        This is useful for iteration over a matrix where the row and column
        indices should be kept track of. For example, if the row and column
        index don't need to be unpacked ::

            >>> m = Matrix([[1, 2], [3, 4]], default=0)
            >>> for key, value in m.items():
            ...     print(f"{key}: {value}")
            ...
            (0, 0): 1
            (0, 1): 2
            (1, 0): 3
            (1, 1): 4

        If the row and key values should be unpacked this can be achieved by
        further tuple unpacking ::

            >>> for (row, col), val in m.items():
            ...     print(f"{row}, {col}: {val}")
            ...
            0, 0: 1
            0, 1: 2
            1, 0: 3
            1, 1: 4

        :param by: The direction in which the matrix values should be
            serialised into a flat sequence, row-wise or column-wise.
        :returns: A list with pairs of the matrix's keys and corresponding
            values.
        """
        if by == "row":
            return [((r, c), self._data[r][c]) for r in self._rowrange for c in self._colrange]
        elif by == "col":
            return [((r, c), self._data[r][c]) for c in self._colrange for r in self._rowrange]
        raise TypeError("Argument 'by' must be literal 'row' or 'col'")

    # DATA GETTERS AND SETTERS

    def submatrix(self, rows: IndexT, cols: IndexT) -> Self:
        """Return a submatrix bounded by *rows* and *cells*."""
        return self._getslice(rows, cols)
        # rows = self._rowtoindices(rows)
        # cols = self._coltoindices(cols)
        # shape = (len(rows), len(cols))
        # data = [self._data[row][col] for row in rows for col in cols]
        # return Matrix(data, shape, default=self._default)

    def _getitem(self, row: int, col: int) -> T:
        """Get a single item."""
        self._check_rowindex(row)
        self._check_colindex(col)
        return self._data[row][col]

    def _setitem(self, row: int, col: int, value: T) -> None:
        """Set a single item."""
        self._check_rowindex(row)
        self._check_colindex(col)
        self._data[row][col] = value

    def _getslice(self, row: IndexT, col: IndexT) -> Self:
        rows = self._rowtoindices(row)
        cols = self._coltoindices(col)
        return self.__class__(  # type: ignore
            [[self._data[r][c] for c in cols] for r in rows],
            default=self._default
        )

    def _setslice(
            self,
            row: IndexT,
            col: IndexT,
            values: Sequence[Sequence[T]] | Sequence[T] | MatrixABC[T]
    ) -> None:
        rows = self._rowtoindices(row)
        cols = self._coltoindices(col)
        cells = [(r, c) for r in rows for c in cols]
        flat_values: Sequence[T]
        if isinstance(values, MatrixABC):
            flat_values = values.values()
        elif isinstance(values, Sequence):
            if len(values) > 0 and all(isinstance(x, Sequence) for x in values):
                values = cast(Sequence[Sequence[T]], values)
                flat_values = list(chain(*values))
            else:
                values = cast(Sequence[T], values)
                flat_values = values
        else:
            raise TypeError(
                "Argument 'values' must be of type Sequence[T], "
                f"Sequence[Sequence[T]], or MatrixT, not {type(values)}"
            )
        if len(flat_values) != len(cells):
            raise ValueError(
                f"Attempting to assign {len(flat_values)} values to {len(cells)} cells"
            )
        for (row, col), value in zip(cells, flat_values, strict=True):
            self._setitem(row, col, value)

    @overload
    def get(self, row_or_key: tuple[int, int]) -> T:
        ...

    @overload
    def get(self, row_or_key: tuple[slice | tuple[int, ...], int]) -> Self:
        ...

    @overload
    def get(self, row_or_key: tuple[int, slice | tuple[int, ...]]) -> Self:
        ...

    @overload
    def get(self, row_or_key: tuple[slice | tuple[int, ...], slice | tuple[int, ...]]) -> Self:
        ...

    @overload
    def get(self, row_or_key: int, col: int) -> T:
        ...

    @overload
    def get(self, row_or_key: slice | tuple[int, ...], col: int) -> Self:
        ...

    @overload
    def get(self, row_or_key: int, col: slice | tuple[int, ...]) -> Self:
        ...

    @overload
    def get(self, row_or_key: slice | tuple[int, ...], col: slice | tuple[int, ...]) -> Self:
        ...

    def get(self,
            row_or_key: IndexT | tuple[IndexT, IndexT],
            col: IndexT | None = None) -> T | Self:
        """Return an item or submatrix based on row and colum indices.

        Can be invoked as either :code:`get((row, col))` or
        :code:`get(row, col)`.

        Returns the value of a cell if both *rows* and *cols* are integers
        which together reference a unique cell. Returns a submatrix if either
        *rows*, *cols* or both are slice objects or tuples of integers with
        several row/column indices.

        :param row_or_key: The row index or row indices (as a tuple or slice)
            of the row(s) to be returned, or a tuple with :code:`(row, col)`
            argument values if *col* is omitted.
        :param col: The column index or column indices (as a tuple or slice) of
            the column(s) to be returned.
        :returns: The value of the matrix cell if both *row* and *col* are
            integers refering to a single cell, otherwise a submatrix covering
            the are selected by *row* and *col*.
        """
        row = row_or_key
        if col is None and isinstance(row, tuple) and len(row) == 2:
            (row, col) = row
        if not (
            (
                isinstance(row, (slice, int))
                or (isinstance(row, tuple) and all(isinstance(x, int) for x in row))
            )
            and
            (
                isinstance(col, (slice, int))
                or (isinstance(col, tuple) and all(isinstance(x, int) for x in col))
            )
        ):
            raise TypeError(
                "Matrix indices must be tuples of type (int | slice | tuple[int, ...], int | slice "
                f"| tuple[int, ...]), not ({type(row)}, {type(col)})"
            )
        row = cast(slice | int | tuple[int, ...], row)  # inference from logic above fails here
        if isinstance(row, (slice, tuple)) or isinstance(col, (slice, tuple)):
            return self._getslice(row, col)
        return self._getitem(row, col)

    def __getitem__(self, key: tuple[IndexT, IndexT]) -> T | Self:
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError(
                "Matrix indices must be tuples of type (int | slice | tuple[int, ...], int | slice "
                f"| tuple[int, ...]), not {type(key)}"
            )
        return self.get(key[0], key[1])

    def __iter__(self) -> Iterator[tuple[int, int]]:
        return iter(self.keys())

    # DUNDER METHODS

    def __str__(self) -> str:
        return DefaultFormatter(self)

    def __repr__(self) -> str:
        return "".join((
            f"{self.__class__.__name__}((",
            *(f"{tuple(row)!r}," for row in self._data),
            f"), default={self._default!r})"
        ))

    def __eq__(self, other: MatrixABC[Any] | Sequence[Sequence[Any]] | Any) -> bool:
        if isinstance(other, MatrixABC):
            return self._data == other._data
        if isinstance(other, Sequence):
            if self._shape == (0, 0) and len(other) == 0:
                return True
            if all(list(other[r]) == self._data[r] for r in range(0, len(other))):
                return True
            return False
        return bool(self._data == other)

    def __bool__(self) -> bool:
        if self._shape[0] == 0 or self._shape[1] == 0:
            return False
        return any(
            self._data[r][c] != self._default for c in self._colrange for r in self._rowrange
        )

    def __len__(self) -> int:
        return self._shape[0] * self._shape[1]

    def __contains__(self, item: T) -> bool:
        return any(item in self._data[r] for r in self._rowrange)

    def __add__(self, other: MatrixABC[V] | V) -> Self | MatrixABC[V]:
        if isinstance(other, MatrixABC):
            return self.matadd(other)
        return self.scaladd(other)

    def __sub__(self, other: MatrixABC[V] | V) -> Self | MatrixABC[V]:
        if isinstance(other, MatrixABC):
            return self.matsub(other)
        return self.scalsub(other)

    def __mul__(self, other: V) -> Self | MatrixABC[V]:
        return self.scalmul(other)

    def __rmul__(self, other: V) -> Self | MatrixABC[V]:
        return self.scalmul(other)

    def __matmul__(self, other: MatrixABC[V]) -> Self | MatrixABC[V]:
        return self.matmul(other)
