import pytest  # noqa: F401
from matrix_types import FrozenMatrix
from common import (
    CommonInitTests, CommonGetterTests, CommonShapeTests,
    CommonRowOperationTests, CommonColumnOperationTests,
    CommonDataAccessTests, CommonOperationTests,
    CommonDunderTests
)


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


class TestRowOperations(CommonRowOperationTests):

    MatrixClass = FrozenMatrix

    def test_insertrow_immutability(self):
        """Check that insertrow doesn't modify or return `self`."""
        m = self._make_2x3_test_matrix()
        t = m.insertrow(0, [-1, -2, -3])
        assert t is not m
        assert t._shape == (3, 3)
        assert m._shape == (2, 3)
        assert t.get(0, 0) == -1
        assert m.get(0, 0) != -1

    def test_prependrow_immutability(self):
        """Check that prenedrow doesn't modify or return `self`."""
        m = self._make_2x3_test_matrix()
        t = m.prependrow([-1, -2, -3])
        assert t is not m
        assert t._shape == (3, 3)
        assert m._shape == (2, 3)
        assert t.get(0, 0) == -1
        assert m.get(0, 0) != -1

    def test_appendrow_immutability(self):
        """Check that appendrow doesn't modify or return `self`."""
        m = self._make_2x3_test_matrix()
        t = m.appendrow([-1, -2, -3])
        assert t is not m
        assert t._shape == (3, 3)
        assert m._shape == (2, 3)
        assert t.get(2, 0) == -1
        with pytest.raises(IndexError) as excinfo:
            m.get(2, 0)
        assert "range" in str(excinfo.value)

    def test_swaprow_immutability(self):
        """Check that swaprow doesn't modify or return `self`."""
        m = self.MatrixClass([[1, 1], [2, 2], [3, 3], [4, 4]], default=0)
        t = m.swaprows(1, 3)
        assert t is not m
        assert t._shape == (4, 2)
        assert m._shape == (4, 2)
        assert t.get(0, 0) == 1
        assert t.get(1, 1) == 4
        assert t.get(2, 0) == 3
        assert t.get(3, 1) == 2
        assert m.get(0, 0) == 1
        assert m.get(1, 1) == 2
        assert m.get(2, 0) == 3
        assert m.get(3, 1) == 4

    def test_removerow_immutability(self):
        """Check that removerow doesn't modify or return `self`."""
        m = self.MatrixClass([[1, 1], [2, 2], [3, 3], [4, 4]], default=0)
        t = m.removerow(1)
        assert t is not m
        assert t._shape == (3, 2)
        assert m._shape == (4, 2)
        assert t.get(0, 0) == 1
        assert t.get(1, 0) == 3
        assert t.get(2, 0) == 4
        assert m.get(0, 0) == 1
        assert m.get(1, 0) == 2
        assert m.get(2, 0) == 3
        assert m.get(3, 0) == 4
        with pytest.raises(IndexError) as excinfo:
            t.get(3, 0)
        assert "range" in str(excinfo.value)


class TestMatrixColumnOperations(CommonColumnOperationTests):

    MatrixClass = FrozenMatrix

    # @TODO: Add immutability tests


class TestDataAccess(CommonDataAccessTests):

    MatrixClass = FrozenMatrix


class TestOperations(CommonOperationTests):

    MatrixClass = FrozenMatrix

    def test_map_immutability(self):
        """Test FrozenMatrix.map() doesn't modify or return `self`."""
        m = self._make_3x3_test_matrix()
        t = m.map(lambda a: a**2)
        assert t is not m
        assert m.aslist() == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


class TestDunders(CommonDunderTests):

    MatrixClass = FrozenMatrix
