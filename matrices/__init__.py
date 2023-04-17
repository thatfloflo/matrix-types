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
from ._base import MatrixABC
from ._matrix import Matrix
from ._frozen_matrix import FrozenMatrix
from typing import TypeAlias

MatrixT: TypeAlias = Matrix | FrozenMatrix | MatrixABC
"""Type alias for matrix types in `matrices`.

This type alias can be used for type annotations whenever any of the matrix
types (e.g. :class:`Matrix`, :class:`FrozenMatrix`) would acceptable.

This includes potentially user-defined subclasses based off :class:`MatrixABC`.
"""

__all__ = [
    "MatrixABC",
    "Matrix",
    "FrozenMatrix",
    "MatrixT",
    "MISSING"
]
