"""Simple matrices for Python.

This package provides two simple two-dimensional matrix types:
:class:`Matrix` is mutable and :class:`FrozenMatrix` is immutable. Both matrix
types support most common matrix operations as well as optionally labelled
rows and columns.

The package also provides an implementation of a sentinel `MISSING` value which
can be used where the absence of a value in a Matrix needs to be signified as a
value distinct from options such as `0`, `None`, etc. A generic type alias
`MatrixT` is also provided, which can be used for type annotations where both
:class:`Matrix` and :class:`FrozenMatrix` would be acceptable.
"""
from ._types import MISSING
from ._matrix import Matrix
from ._frozen_matrix import FrozenMatrix
from typing import TypeAlias

MatrixT: TypeAlias = Matrix | FrozenMatrix

__all__ = [
    "Matrix",
    "FrozenMatrix",
    "MatrixT",
    "MISSING"
]
