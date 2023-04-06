"""Simple matrices for Python.

This module provides two simple two-dimensional matrix types:
`Matrix` is mutable and `FrozenMatrix` is immutable. Both matrix types support
most common matrix operations as well as optionally labelled rows and/or
columns.
"""
from typing import TypeAlias
from ._types import MISSING, T
from ._base import Matrix
# from ._matrix import Matrix
# from ._frozen_matrix import FrozenMatrix

# MatrixType: TypeAlias = Matrix[T] | FrozenMatrix[T]

__all__ = [
    "Matrix",
    # "FrozenMatrix",
    # "MatrixType",
    "MISSING"
]
