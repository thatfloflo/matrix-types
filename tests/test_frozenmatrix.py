import pytest  # noqa: F401
from matrix_types import FrozenMatrix
from common import CommonInitTests, CommonGetterTests, CommonShapeTests


class TestInit(CommonInitTests):

    MatrixClass = FrozenMatrix


class TestGetters(CommonGetterTests):

    MatrixClass = FrozenMatrix


class TestMatrixShapes(CommonShapeTests):

    MatrixClass = FrozenMatrix

    def test_transpose_immutability(self):
        """Check that transpose doesn't modify or return `self`."""
        m = self._make_2x3_test_matrix()
        t = m.transpose()
        assert t is not m
        self._check_2x3_values(m)  # Make sure it didn't transpose

    def test_resize_immutability(self):
        """Check that resize doesn't modify or return `self`."""
        m = self._make_2x3_test_matrix()
        t = m.resize(4, 4)
        assert t is not m
        assert m._shape != (4, 4)
        assert t._shape == (4, 4)

    def test_flip_immutability(self):
        """Check that flip doesn't modify or return `self`."""
        m = self.MatrixClass([[1, 1], [2, 2], [3, 3]], default=0)
        t = m.flip()
        assert t is not m
        assert m._shape == (3, 2)
        assert t._shape == (3, 2)
        assert m.get(0, 0) == 1
        assert t.get(0, 0) == 3

    def test_flipv_immutability(self):
        """Check that flipv doesn't modify or return `self`."""
        m = self._make_2x3_test_matrix()
        t = m.flipv()
        assert t is not m
        self._check_2x3_values(m)  # Make sure it didn't flip

    def test_fliph_immutability(self):
        """Check that fliph doesn't modify or return `self`."""
        m = self._make_2x3_test_matrix()
        t = m.fliph()
        assert t is not m
        self._check_2x3_values(m)  # Make sure it didn't flip
