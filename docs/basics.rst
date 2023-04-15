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

      Constructing matrix objects from a flat sequence:

      .. code:: python
         
         from matrix_types import Matrix, FrozenMatrix

         # Matrices with 2 rows, 3 columns, and all cells filled with '0'
         a = Matrix([], (2, 3), default=0)
         b = FrozenMatrix([], (2, 3), default=0)

         # 2x2 matrices of the form
         #    1  2
         #    3  4
         c = Matrix([1, 2, 3, 4], (2, 2), default=0)
         d = FrozenMatrix(range(100), (2, 2), default=0)

      Constructing matrix objects from sequences of sequences:

      .. code:: python

         ...

      Constructing matrix objects from other matrix objects:

      .. code:: python

         ...

   :param MatrixABC[T] | Sequence[T] | Sequence[Sequence[T]] data: The data to
      be used to fill in the initial values of the matrix.
   :param tuple[int, int] shape: The shape the matrix should have in the
      format :code:`(rows, cols)`. Obligatory if *data* is a flat sequence.
   :param T default: Keyword-only argument specifying the default value to be
      used for cells that otherwise have not been assigned any value. Also used
      to evaluate semantically whether a cell (or entire matrix) is
      interpreted as *empty* or not.
   :rtype: Matrix[T] | FrozenMatrix[T]
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

.. py:function:: m.shape()

   Return the shape of the matrix object as a tuple of the form
   :code:`(rows, cols)`.

   :rtype: tuple[int, int]

.. py:function:: len(m)

   Return the number of items (cells) in the matrix. This is always the product
   of the number of rows and the number of columns, e.g. for a 5x10 matrix this
   would be *5 \* 10 =* **50**.

   :rtype: int