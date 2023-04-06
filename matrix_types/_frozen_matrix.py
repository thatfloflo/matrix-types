"""Frozen matrices."""
from ._base import MatrixType
from ._types import T


class FrozenMatrix(MatrixType[T]):
    ...
