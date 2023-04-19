The Matrix Types --- *Matrix* and *FrozenMatrix*
================================================

Constructing matrix objects
---------------------------

The constructors for both classes work the same way:

.. py:class:: Matrix(data [, shape, *, default])

.. py:class:: FrozenMatrix(data [, shape, *, default])

   Return a new :class:`Matrix` or :class:`FrozenMatrix` object, whose cell
   values are taken from *data*.

   Matrices can be created in several different ways:

   * From an existing :class:`Matrix` or :class:`FrozenMatrix` instance: :code:`Matrix(m)`.
   * From a sequence of sequences: :code:`Matrix([[1, 2, 3], [4, 5, 6]], default=0)`.
   * From a simple sequence: :code:`Matrix([1, 2, 3, 4, 5, 6], shape=(2, 3), default=0)`.

   When constructing a new :class:`Matrix` or :class:`FrozenMatrix` object from
   an existing :class:`Matrix` or :class:`FrozenMatrix` instance, both the
   *shape* and *default* arguments are optional. If they are not specified,
   they will be copied over from the matrix passed as *data*.
   If *shape* is specified, the new matrix will be reshaped by internally
   calling :func:`resize()` to resize the matrix.
   If *default* is specified this will be used as the new default value, but
   cells with the default already in *data* will never be altered.

   When constructing a new :class:`Matrix` or :class:`FrozenMatrix` object from
   a sequence of sequences, it is assumed that these are in the form of a
   sequence of rows, with each row being a sequence of column values. The
   *shape* argument is optional, and if not specified will be inferred based on
   the number of 'row-sequences' and the number of 'column-items' in the first
   'row-sequence'. If *shape* is specified and does not match the inferred size,
   then the data is padded with *default* where too few items are found, while
   items exceeding the expected number are ignored.
   The *default* argument is obligatory because there is no reliable way of
   inferring an appropriate default value from a regular sequence.
   
   When constructing a new :class:`Matrix` or :class:`FrozenMatrix` object from
   a 'flat' sequence, both the *shape* and *default* arguments are obligatory
   as they cannot be inferred from a regular sequence.
   The values taken from *data* are used to fill the matrix row-wise. Left-over
   values in *data* are ignored, and any remaining cells are padded with
   *default*.
   This offers a very useful pattern for constructing matrices with a single
   value by passing an empty sequence as *data*, e.g. to construct a 3x3
   zero-matrix, we can call :code:`Matrix([], (3, 3), default=0)`.

   :Examples:

      .. code-block:: python
         :caption: Constructing matrix objects from a flat sequence
         
         from matrices import Matrix, FrozenMatrix

         # Matrices with 2 rows, 3 columns, and all cells filled with '0'
         a = Matrix([], (2, 3), default=0)
         b = FrozenMatrix([], (2, 3), default=0)

         # 2x2 matrices of the form
         #    1  2
         #    3  4
         c = Matrix([1, 2, 3, 4], (2, 2), default=0)
         d = FrozenMatrix(range(100), (2, 2), default=0)

      .. code-block:: python
         :caption: Constructing matrix objects from sequences of sequences

         from matrices import Matrix, FrozenMatrix

         # 2x2 matrices of the form
         #    1  2
         #    3  4
         a = Matrix([[1, 2], [3, 4]], default=0)  # The shape can be inferred
         b = FrozenMatrix([[1, 2] [3, 4]], (2, 2), default=0)  # Explicit shape

      .. code-block:: python
         :caption: Constructing matrix objects from other matrix objects

         from matrices import Matrix, FrozenMatrix

         # 2x2 matrices of the form
         #    1  2
         #    3  4
         a = Matrix([[1, 2], [3, 4]], default=0)  # Construct mutable matrix
         b = FrozenMatrix(a)  # Immutable copy of a

   :param MatrixABC[~T] | Sequence[~T] | Sequence[Sequence[~T]] data: The data to
      be used to fill in the initial values of the matrix.
   :param tuple[int, int] shape: The shape the matrix should have in the
      format :code:`(rows, cols)`. Obligatory if *data* is a flat sequence.
   :param ~T default: Keyword-only argument specifying the default value to be
      used for cells that otherwise have not been assigned any value. Also used
      to evaluate semantically whether a cell (or entire matrix) is
      interpreted as *empty* or not.
   :rtype: Matrix[~T] | FrozenMatrix[~T]
   :returns: Returns a new :class:`Matrix` or :class:`FrozenMatrix` object.


Differences between :class:`Matrix` and :class:`FrozenMatrix`
-------------------------------------------------------------

The principal difference between :class:`Matrix` and :class:`FrozenMatrix`
objects is that the former are mutable and the latter are immutable.

Whereas many methods on :class:`Matrix` modify the matrix in-place and return
the modified object itself, :class:`FrozenMatrix` always returns a modified
*copy* of itself instead.

In line with this, :class:`FrozenMatrix` does not implement key-based
assignment (e.g. :code:`m[0, 0] = 123`) and in-place operands (e.g.
:code:`m *= 3`), because this is not compatible with the *copy-on-modification*
approach.

If you want to write code which is compatible with both :class:`Matrix` and
:class:`FrozenMatrix`, it is thus important to always implicitly assign your
results. For instance::

    def good(m: MatrixABC) -> None:
        # This will work with both Matrix and FrozenMatrix
        m = m.resize(4, 4)
        print(m[3, 3])

    def bad(m: MatrixABC) -> None:
        # This will not work with FrozenMatrix
        m.resize(4, 4)
        print(m[3, 3])

    a = Matrix([1, 2, 3, 4, 5, 6], (3, 3), default=0)
    b = FrozenMatrix(a)
    good(a) # Success: prints '0'
    bad(a)  # Success: prints '0'
    good(b) # Success: prints '0'
    bad(b)  # Failure: raises IndexError


.. important:: *Immutability is imperfect!*

   While :class:`FrozenMatrix` does not provide any public functionality that
   would alter a specific instance of FrozenMatrix, and all operations
   affecting the matrix's shape or values result in copies, Python itself does
   not offer any mechanism to truly prevent user code from modifying the
   internals of an object (e.g. by accessing and modifying the internal data
   structure directly).
   
   This means that immutability with :class:`FrozenMatrix` can be *assumed*,
   but cannot be *guaranteed*, because user code could potentially attempt to
   modify the internals of the object, even if that is very poor practice and
   to be discouraged in the strongest terms.
   
   You should *never* write code that modifies the internals (any attributes
   whose name starts with an underscore) on an already-instantiated object. If
   you ever have the need to access or modify the internals of a matrix object,
   you should subclass :class:`MatrixABC`, :class:`Matrix`, or
   :class:`FrozenMatrix` instead, and retain that functionality within your
   subclass, so that assurances about mutability/immutability can be
   maintained for all matrix objects.


Basic properties of matrix objects
----------------------------------

.. py:function:: bool(m)

   Return :code:`True` *iff* any of the cells of the matrix contain a value
   other than the current *default* value.

   Always returns :code:`False` for matrices with a zero dimension (i.e.
   matrices with the shapes 0x0, *n*\ x0, and 0x\ *n*).

   For the inverse of :obj:`bool(m)`, see :func:`m.empty()`.

   .. note::
      Note that this behaviour may lead to two matrices with the same values
      comparing as equal, while one of these matrices evaluates as :code:`True`
      and the other as :code:`False`, namely if they have different default
      values.

      :Example:

         .. code-block:: python
         
            a = Matrix([1, 1, 1, 1], (2, 2), default=0)
            b = Matrix([1, 1, 1, 1], (2, 2), default=1)

            a == b  # Evaluates to True, because both matrices have the same values
            bool(a) # Evaluates to True, because at least one of the values is not 0
            bool(b) # Evaluates to False, because all the values are 1 (the default)

   :rtype: bool

.. py:property:: m.default

   The current default value of the matrix.

   *Read-only* on immutable :class:`FrozenMatrix` objects,
   *read-write* on mutable :class:`Matrix` objects.

   Altering the default will *never* affect the data already present in a
   matrix, it will only affect value comparisons and new values inserted after
   the default was modified. For example::

      >>> a = Matrix([], (3, 3), default=0)
      >>> a.empty()
      True
      >>> a.default = 1
      >>> a.empty()
      False
      >>> a.resize(4, 4)
      >>> print(a)
           0  1  2  3
        ┌             ┐
      0 │  0  0  0  1 │
      1 │  0  0  0  1 │
      2 │  0  0  0  1 │
      3 │  1  1  1  1 │
        └             ┘

   To change the default value on immutable :class:`FrozenMatrix` objects, you
   must create a new :class:`FrozenMatrix` object with the *default* property
   overwritten. For example::

      >>> a = FrozenMatrix([], (3, 3), default=0)
      >>> bool(a)
      False
      >>> b = FrozenMatrix(a, default=1)  # a with the default overwritten
      >>> bool(b)
      True

   :type: *~T*

.. py:function:: m.empty()

   Return :code:`True` *iff* all of the cells of the matrix are equal to the
   current *default* value, or the matrix has a zero dimension (i.e.
   matrices with the shapes 0x0, *n*\ x0, and 0x\ *n*). Return :code:`False`
   otherwise.

   For the inverse of :func:`m.empty()`, see :obj:`bool(m)`.

   :rtype: bool

.. py:function:: len(m)

   Return the number of items (cells) in the matrix. This is always the product
   of the number of rows and the number of columns, e.g. for a 5x10 matrix this
   would be *5 \* 10 =* **50**.

   :rtype: int

.. py:property:: m.shape

   The current shape of the matrix in the form :code:`(rows, cols)`.

   *Read-only* on immutable :class:`FrozenMatrix` objects,
   *read-write* on mutable :class:`Matrix` objects.

   To alter the shape on :class:`FrozenMatrix` objects, use :func:`m.resize()`
   or make a new object with the *shape* property overwritten instead.

   :type: tuple[int, int]


Row and column manipulation
---------------------------

Shape modifications, such as the addition, removal, or swapping of rows or
columns are a mainstay when working with matrices. The |project| package
provides a number of convenient functions to accomplish this.

.. py:function:: m.appendcol(data)

   Append a column with values *data* to the right of the matrix.

   :param Sequence[~T] data: The values to be inserted in the new column.
   :rtype: Self
   :returns: Mutable :class:`Matrix` objects return *self*, immutable
      :class:`FrozenMatrix` objects return a modified copy of *self*.

.. py:function:: m.appendrow(data)

   Append a row with values *data* to the bottom of the matrix.

   :param Sequence[~T] data: The values to be inserted in the new row.
   :rtype: Self
   :returns: Mutable :class:`Matrix` objects return *self*, immutable
      :class:`FrozenMatrix` objects return a modified copy of *self*.

.. py:function:: m.flip(* [, by])

   Flip the order a matrix's rows or columns.

   If *by* is :code:`"row"` (the default), then the order of the rows in the
   matrix will be flipped (i.e. reversed). If *by* is :code:`col`, then the
   order of the columns in the matrix will be flipped.

   :Examples:

      .. code-block:: python
         :caption: Flipping rows

         m = FrozenMatrix([[1, 1], [2, 2]], default=0)
         print(m)
         # Output:
         #      0  1
         #    ┌      ┐
         #  0 │ 1  1 │
         #  1 │ 2  2 │
         #    └      ┘
         print(m.flip())
         # Output:
         #      0  1
         #    ┌      ┐
         #  0 │ 2  2 │
         #  1 │ 1  1 │
         #    └      ┘

      .. code-block:: python
         :caption: Flipping columns

         m = FrozenMatrix([[1, 2], [1, 2]], default=0)
         print(m)
         # Output:
         #      0  1
         #    ┌      ┐
         #  0 │ 1  2 │
         #  1 │ 1  2 │
         #    └      ┘
         print(m.flip(by="col"))
         # Output:
         #      0  1
         #    ┌      ┐
         #  0 │ 2  1 │
         #  1 │ 2  1 │
         #    └      ┘

   :param RowColT by: One of the literals :code:`"row"` (the default) or
      :code:`"col"`, specifies whether the matrix should be flipped row-wise
      or column-wise.
   :rtype: Self
   :returns: Mutable :class:`Matrix` objects return *self*, immutable
      :class:`FrozenMatrix` objects return a flipped copy of *self*.

.. py:function:: m.fliph()

   Alias for :code:`m.flip(by="col")`.

.. py:function:: m.flipv()

   Alias for :code:`m.flip(by="row")`.

.. py:function:: m.insertcol(index, data)

   Insert a column with values *data* to the left of the column referenced by
   *index*.

   :param int index: The column index before which the new column should be
      inserted.
   :param Sequence[~T] data: The values to be inserted in the new column.
   :rtype: Self
   :returns: Mutable :class:`Matrix` objects return *self*, immutable
      :class:`FrozenMatrix` objects return a modified copy of *self*.

.. py:function:: m.insertrow(index, data)

   Insert a row with values *data* to the top of the row referenced by
   *index*.

   :param int index: The row index before which the new row should be inserted.
   :param Sequence[~T] data: The values to be inserted in the new row.
   :rtype: Self
   :returns: Mutable :class:`Matrix` objects return *self*, immutable
      :class:`FrozenMatrix` objects return a modified copy of *self*.

.. py:function:: m.prependcol(data)

   Prepend a column with values *data* at the left of the matrix.

   :param Sequence[~T] data: The values to be inserted in the new column.
   :rtype: Self
   :returns: Mutable :class:`Matrix` objects return *self*, immutable
      :class:`FrozenMatrix` objects return a modified copy of *self*.

.. py:function:: m.prependrow(data)

   Prepend a row with values *data* at the top of the matrix.

   :param Sequence[~T] data: The values to be inserted in the new row.
   :rtype: Self
   :returns: Mutable :class:`Matrix` objects return *self*, immutable
      :class:`FrozenMatrix` objects return a modified copy of *self*.

.. py:function:: m.removecol(index)

   Remove the column at *index*.

   .. caution::

      The column is *removed completely* from the matrix, and the matrix’s
      shape will be altered. Calling this function does not merely reset the
      values of items in the targeted column to their default!

   :param int index: The index of the column to be removed.
   :rtype: Self
   :returns: Mutable :class:`Matrix` objects return *self*, immutable
      :class:`FrozenMatrix` objects return a modified copy of *self*.

.. py:function:: m.removerow(index)

   Remove the row at *index*.

   .. caution::

      The row is *removed completely* from the matrix, and the matrix’s
      shape will be altered. Calling this function does not merely reset the
      values of items in the targeted row to their default!

   :param int index: The index of the row to be removed.
   :rtype: Self
   :returns: Mutable :class:`Matrix` objects return *self*, immutable
      :class:`FrozenMatrix` objects return a modified copy of *self*.

.. py:function:: m.resize(rows, cols)
.. py:function:: m.resize(shape)
   :noindex:

   Grow or shrink a matrix.

   Grows or shrinks the matrix depending on whether the new *shape*'s *rows* or
   *cols* are less than or greater than the current row or column count. Has no
   effect on the shape if they match the current row and column count.

   Where the new shape has fewer rows or columns the values from these will be
   lost. Where the new shape has additional rows or columns, these will be
   populated with :attr:`m.default`.

   :param tuple[int, int] shape: Positional-only argument specifying the shape
      of the resized matrix in the form :code:`(rows, cols)`.
   :param int rows: The number of rows the matrix should have after resizing.
   :param int cols: The number of columns the matrix should have after
      resizing.
   :rtype: Self
   :returns: Mutable :class:`Matrix` objects return *self*, immutable
      :class:`FrozenMatrix` objects return a modified copy of *self*.

.. py:function:: m.swapcols(a_index, b_index)

   Swap the two columns with indices *a_index* and *b_index*.

   :Example:

      >>> a = Matrix([[0, 1, 2], [0, 1, 2]], default=0)
      >>> print(a)
          0  1  2
        ┌         ┐
      0 │ 0  1  2 │
      1 │ 0  1  2 │
        └         ┘
      >>> print(a.swapcols(0, 2))
          0  1  2
        ┌         ┐
      0 │ 2  1  0 │
      1 │ 2  1  0 │
        └         ┘

   :param int a_index: The column index of the first column to be swapped.
   :param int b_index: The column index of the second column to be swapped.
   :rtype: Self
   :returns: Mutable :class:`Matrix` objects return *self*, immutable
      :class:`FrozenMatrix` objects return a modified copy of *self*.

.. py:function:: m.swaprows(a_index, b_index)

   Swap the two rows with indices *a_index* and *b_index*.

   :Example:

      >>> a = Matrix([[0, 0], [1, 1], [2, 2]], default=0)
      >>> print(a)
          0  1
        ┌      ┐
      0 │ 0  0 │
      1 │ 1  1 │
      2 │ 2  2 │
        └      ┘
      >>> print(a.swaprows(0, 2))
          0  1
        ┌      ┐
      0 │ 2  2 │
      1 │ 1  1 │
      2 │ 0  0 │
        └      ┘

   :param int a_index: The row index of the first row to be swapped.
   :param int b_index: The row index of the second row to be swapped.
   :rtype: Self
   :returns: Mutable :class:`Matrix` objects return *self*, immutable
      :class:`FrozenMatrix` objects return a modified copy of *self*.

.. py:function:: m.transpose()

   Transpose the rows and columns of the matrix.

   In a transposed matrix, the first row is converted to the first column,
   the second row is converted to the second column, and so on.
   Transposing a matrix twice in a row always returns it to its original form.

   This turns a matrix of the form
   :math:`\begin{bmatrix}1 & 2 & 3\\4 & 5 & 6\end{bmatrix}`
   into a matrix of the form
   :math:`\begin{bmatrix}1 & 4\\ 2 & 5\\3 & 6\end{bmatrix}`.
   

   :rtype: Self
   :returns: Mutable :class:`Matrix` objects return *self*, immutable
      :class:`FrozenMatrix` objects return a modified copy of *self*.


Accessing values in a matrix
----------------------------

.. py:function:: m.copy()

   Return a shallow copy of the matrix.

   :rtype: Self
   :returns: Returns a shallow copy of *self*.

.. py:function:: m.get(row, col)
.. py:function:: m.get(key)
   :noindex:
.. py:function:: m[row, col]
.. py:function:: m[key]

   TO BE WRITTEN

   :param tuple[IndexT, IndexT] key: A tuple of *row* and *col* indeces.
   :param IndexT row: The row index for the cell(s) to retreive, can be an
      integer to refer to a single row, a slice to refer to a subset of rows,
      or a tuple of row indices to select any arbitrary number of rows.
   :param IndexT col: The column index for the cell(s) to retreive, can be an
      integer to refer to a single column, a slice to refer to a subset of
      columns, or a tuple of column indices to select any arbitrary number of
      columns.
   :rtype: ~T | Matrix[~T] | FrozenMatrix[~T]
   :returns: Returns the value of the cell specified by *row*, *col* if these
      refer to a single cell (i.e. both *row* and *cell* are single integers),
      otherwise returns a new :class:`Matrix` or :class:`FrozenMatrix` object
      containing the selected rows and column (possibly 0x0, *n*\ x0 or
      0x\ *n*), following standard Python slice logic and intersecting the
      slices where appropriate.

.. py:function:: m.items(* [, by])

   TO BE WRITTEN

   See also :func:`m.asdict()` for a method which returns the same data as
   a dictionary rather than a list of tuples.

   :param RowColT by: One of the literals :code:`"row"` (the default) or
      :code:`"col"`, specifies whether the list of key-value pairs should be
      constructed by row-wise or column-wise iteration of the matrix.
   :rtype: list[tuple[tuple[int, int], ~T]]
   :returns: Returns a list of tuples where the first member of each tuple is
      a key tuple (a tuple with indices of the form :code:`(row, col)`) and the
      second member of the tuple is the value of the cell indexed by that key.
      The list is ordered row-wise or column-wise depending on *by*.

.. py:function:: m.keys(* [, by])

   TO BE WRITTEN

   :param RowColT by: One of the literals :code:`"row"` (the default) or
      :code:`"col"`, specifies whether the list of keys should be constructed
      by row-wise or column-wise iteration of the matrix.
   :rtype: list[tuple[int, int]]
   :returns: Returns a list of tuples with all the keys (aka row and column
      indices) of the matrix, ordered row-wise or column-wise depending on
      *by*. Each tuple has the form :code:`(row, col)`.

.. py:function:: m.values(* [, by])

   TO BE WRITTEN

   :param RowColT by: One of the literals :code:`"row"` (the default) or
      :code:`"col"`, specifies whether the list of values should be constructed
      by row-wise or column-wise iteration of the matrix.
   :rtype: list[~T]
   :returns: Returns a list of all the cell values in the matrix, ordered
      row-wise or column-wise depending on *by*.

.. py:function:: submatrix(rows, cols)

   TO BE WRITTEN

Iteration over matrices
-----------------------

.. py:function:: m.foreach(func [, *args, **kwargs])

   TO BE WRITTEN

.. py:function:: iter(m)

   TO BE WRITTEN

.. py:function:: m.map(func [, *args, **kwargs])

   TO BE WRITTEN


Common operations on matrices
-----------------------------

.. py:function:: value in m

   TO BE WRITTEN

.. py:function:: m is other

   TO BE WRITTEN

.. py:function:: m == other

   TO BE WRITTEN

.. py:function:: m.matadd(other)
.. py:function:: m.scaladd(scalar)
.. py:function:: m + other
.. py:function:: m + scalar

   TO BE WRITTEN

.. py:function:: m.matmul(other)
.. py:function:: m.scalmul(scalar)
.. py:function:: m @ other
.. py:function:: m * scalar
.. py:function:: scalar * m

   TO BE WRITTEN

.. py:function:: m.matsub(other)
.. py:function:: m.scalsub(scalar)
.. py:function:: m - other
.. py:function:: m - scalar

   TO BE WRITTEN


In-place matrix operations
--------------------------

Most of the common matrix operations also implement an in-place
variant for :class:`Matrix` objects (but obviouslt *not* for
:class:`FrozenMatrix` objects). These modify the matrix in-place
instead of returning a new :class:`Matrix` or :class:`FrozenMatrix`
object.

Scalar in-place operations:

* :code:`m.iscaladd(scalar)`, :code:`m += scalar`, see :func:`m.scaladd()`.
* :code:`m.iscalmul(scalar)`, :code:`m *= scalar`, see :func:`m.scalmul()`.
* :code:`m.iscalsub(scalar)`, :code:`m -= scalar`, see :func:`m.scalsub()`.

Matrix in-place operations:

* :code:`m.imatadd(other)`, :code:`m += other`, see :func:`m.matadd()`.
* :code:`m.imatmul(other)`, :code:`m @= other`, see :func:`m.matmul()`.
* :code:`m.imatsub(other)`, :code:`m -= other`, see :func:`m.matsub()`.

See the respective regular operation. The semantics are the same except for
the result being stored directly in the matrix *m*.


Converting matrices to other formats
------------------------------------

.. py:function:: m.aslist(* [, by])

   TO BE WRITTEN

   See also :func:`m.values()` which returns a flat list of the matrix's
   values.

   :param RowColT by: One of the literals :code:`"row"` (the default) or
      :code:`"col"`, specifies whether the list of lists should be constructed
      by row-wise or column-wise iteration of the matrix. 
   :rtype: list[list[~T]]
   :returns: Returns a list of lists, with the sublists containing the
      values of the matrix either by column or by row, depending on *by*.

.. py:function:: m.asdict()

   TO BE WRITTEN

   :rtype: dict[tuple[int, int], ~T]
   :returns: Returns a dictionary where they keys are tuples of indices of the
      form :code:`(row, col)` and values the values of the cells with that
      index.

.. py:function:: repr(m)

   TO BE WRITTEN

.. py:function:: str(m)

   TO BE WRITTEN
