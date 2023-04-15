The Matrix Types --- *Matrix* and *FrozenMatrix*
================================================

The constructors for both classes work the same way:

.. py:class:: Matrix(data [, shape, *, default])
.. py:class:: FrozenMatrix(data [, shape, *, default])

   Return a new :class:`Matrix` or :class:`FrozenMatrix` object, whose cell
   values are taken from *data*.

   Matrices can be created in several different ways:

   * From an existing :class:`Matrix` or :class:`FrozenMatrix` instance: :code:`Matrix(m)`.
   * From a sequence of sequences: :code:`Matrix([[1, 2, 3], [4, 5, 6]], default=0)`.
   * From a simple sequence: :code:`Matrix([1, 2, 3, 4, 5, 6], shape=(2, 3), default=0)`.