import pytest  # noqa: F401
from matrices import Matrix
from common import (
    CommonTestBase, CommonInitTests, CommonGetterTests, CommonShapeTests,
    CommonRowOperationTests, CommonColumnOperationTests, CommonDataAccessTests,
    CommonOperationTests, CommonDunderTests
)


class TestInit(CommonInitTests):

    MatrixClass = Matrix


class TestGetters(CommonGetterTests):

    MatrixClass = Matrix


class TestShapes(CommonShapeTests):

    MatrixClass = Matrix

    def test_transpose_insitu(self):
        """Check that transpose modifies and returns `self`."""
        m = self._make_2x3_test_matrix()
        t = m.transpose()
        assert t is m
        assert m.get(1, 0) == 2  # Make sure it did transpose
        m.transpose()            # Back to normal
        self._check_2x3_values(m)

    def test_resize_insitu(self):
        """Check that resize modifies and returns `self`."""
        m = self._make_2x3_test_matrix()
        t = m.resize(4, 4)
        assert t is m
        assert m._shape == (4, 4)
        assert t._shape == (4, 4)

    def test_flip_insitu(self):
        """Check that flip modifies and returns `self`."""
        m = self.MatrixClass([[1, 1], [2, 2], [3, 3]], default=0)
        assert m._shape == (3, 2)
        assert m.get(0, 0) == 1
        t = m.flip()
        assert t is m
        assert m._shape == (3, 2)
        assert m.get(0, 0) == 3

    def test_flipv_insitu(self):
        """Check that flipv modifies and returns `self`."""
        m = self.MatrixClass([[1, 1], [2, 2], [3, 3]], default=0)
        t = m.flipv()
        assert t is m

    def test_fliph_insitu(self):
        """Check that fliph modifies and returns `self`."""
        m = self.MatrixClass([[1, 2, 3], [1, 2, 3]], default=0)
        t = m.fliph()
        assert t is m


class TestRowOperations(CommonRowOperationTests):

    MatrixClass = Matrix

    def test_insertrow_insitu(self):
        """Check that insertrow modifies and returns `self`."""
        m = self._make_2x3_test_matrix()
        t = m.insertrow(0, [-1, -2, -3])
        assert t is m
        assert m._shape == (3, 3)
        assert m.get(0, 0) == -1

    def test_prependrow_insitu(self):
        """Check that prenedrow modifies and returns `self`."""
        m = self._make_2x3_test_matrix()
        t = m.prependrow([-1, -2, -3])
        assert t is m
        assert m._shape == (3, 3)
        assert m.get(0, 0) == -1

    def test_appendrow_insitu(self):
        """Check that appendrow modifies and returns `self`."""
        m = self._make_2x3_test_matrix()
        t = m.appendrow([-1, -2, -3])
        assert t is m
        assert m._shape == (3, 3)
        assert m.get(2, 0) == -1
        with pytest.raises(IndexError) as excinfo:
            m.get(3, 0)
        assert "range" in str(excinfo.value)

    def test_swaprow_insitu(self):
        """Check that swaprow modifies and returns `self`."""
        m = self.MatrixClass([[1, 1], [2, 2], [3, 3], [4, 4]], default=0)
        t = m.swaprows(1, 3)
        assert t is m
        assert m._shape == (4, 2)
        assert m.get(0, 0) == 1
        assert m.get(1, 1) == 4
        assert m.get(2, 0) == 3
        assert m.get(3, 1) == 2

    def test_removerow_insitu(self):
        """Check that appendrow modifies and returns `self`."""
        m = self.MatrixClass([[1, 1], [2, 2], [3, 3], [4, 4]], default=0)
        t = m.removerow(1)
        assert t is m
        assert m._shape == (3, 2)
        assert m.get(0, 0) == 1
        assert m.get(1, 0) == 3
        assert m.get(2, 0) == 4
        with pytest.raises(IndexError) as excinfo:
            m.get(3, 0)
        assert "range" in str(excinfo.value)


class TestMatrixColumnOperations(CommonColumnOperationTests):

    MatrixClass = Matrix

    # @TODO: Add in-situ mutability tests


class TestDataAccess(CommonDataAccessTests):

    MatrixClass = Matrix


class TestOperations(CommonOperationTests):

    MatrixClass = Matrix

    def test_imatadd(self):
        """Test in-situ matrix addition."""
        m = self._make_3x3_test_matrix()
        o = self._make_3x3_test_matrix()
        m.imatadd(o)
        assert m.values() == [2, 4, 6, 8, 10, 12, 14, 16, 18]
        assert o.values() == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_imatsub(self):
        """Test in-situ matrix subtraction."""
        m = self._make_3x3_test_matrix()
        o = self._make_3x3_test_matrix()
        m.imatsub(o)
        assert m.values() == [0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert o.values() == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_imatmul(self):
        """Test in-situ matrix multiplication."""
        m = self._make_3x3_test_matrix()
        o = self._make_3x3_test_matrix()
        m.imatmul(o)
        assert m.aslist() == [[30, 36, 42], [66, 81, 96], [102, 126, 150]]
        assert o.values() == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        incompatible = Matrix([], shape=(2, 3), default=0)
        with pytest.raises(ValueError):
            m.imatmul(incompatible)
        with pytest.raises(ValueError):
            incompatible.imatmul(m)
        assert m.aslist() == [[30, 36, 42], [66, 81, 96], [102, 126, 150]]

    def test_iscaladd(self):
        """Test in-situ scalar addition."""
        m = self._make_3x3_test_matrix()
        m.iscaladd(2)
        assert m.aslist() == [[3, 4, 5], [6, 7, 8], [9, 10, 11]]

    def test_iscalsub(self):
        """Test in-situ scalar subtraction."""
        m = self._make_3x3_test_matrix()
        m.iscalsub(2)
        assert m.aslist() == [[-1, 0, 1], [2, 3, 4], [5, 6, 7]]

    def test_iscalmul(self):
        """Test in-situ scalar multiplication."""
        m = self._make_3x3_test_matrix()
        m.iscalmul(2)
        assert m.aslist() == [[2, 4, 6], [8, 10, 12], [14, 16, 18]]

    def test_map_insitu(self):
        """Test Matrix.map() works in-situ and returns `self`."""
        m = self._make_3x3_test_matrix()
        t = m.map(lambda a: a**2)
        assert t is m
        assert m.aslist() == [[1, 4, 9], [16, 25, 36], [49, 64, 81]]


class TestDunders(CommonDunderTests):

    MatrixClass = Matrix

    def test__iadd__(self):
        """Test += / __iadd__."""
        m = self._make_3x3_test_matrix()
        n = self._make_3x3_test_matrix()
        # Matrix addition, same size...
        m += n
        assert n[0, 0] == 1
        assert n[0, 1] == 2
        assert n[0, 2] == 3
        assert n[1, 0] == 4
        assert n[1, 1] == 5
        assert n[1, 2] == 6
        assert n[2, 0] == 7
        assert n[2, 1] == 8
        assert n[2, 2] == 9
        assert m[0, 0] == 1 + 1
        assert m[0, 1] == 2 + 2
        assert m[0, 2] == 3 + 3
        assert m[1, 0] == 4 + 4
        assert m[1, 1] == 5 + 5
        assert m[1, 2] == 6 + 6
        assert m[2, 0] == 7 + 7
        assert m[2, 1] == 8 + 8
        assert m[2, 2] == 9 + 9
        assert m._shape == (3, 3)
        assert n._shape == (3, 3)
        # Matrix addition, different sizes...
        o = self.MatrixClass([[1, 2, 3]], default=0)
        with pytest.raises(ValueError):
            m += o
        p = self.MatrixClass([[1], [2], [3]], default=0)
        with pytest.raises(ValueError):
            m += p
        assert m[0, 0] == 1 + 1
        assert m[1, 1] == 5 + 5
        assert m[2, 2] == 9 + 9
        # Scalar addition
        s = 4
        n += s
        assert n[0, 0] == 1 + s
        assert n[0, 1] == 2 + s
        assert n[0, 2] == 3 + s
        assert n[1, 0] == 4 + s
        assert n[1, 1] == 5 + s
        assert n[1, 2] == 6 + s
        assert n[2, 0] == 7 + s
        assert n[2, 1] == 8 + s
        assert n[2, 2] == 9 + s
        assert n._shape == (3, 3)

    def test__isub__(self):
        """Test -= / __isub__."""
        m = self._make_3x3_test_matrix()
        n = self._make_3x3_test_matrix()
        # Matrix addition, same size...
        m -= n
        assert n[0, 0] == 1
        assert n[0, 1] == 2
        assert n[0, 2] == 3
        assert n[1, 0] == 4
        assert n[1, 1] == 5
        assert n[1, 2] == 6
        assert n[2, 0] == 7
        assert n[2, 1] == 8
        assert n[2, 2] == 9
        assert m[0, 0] == 1 - 1
        assert m[0, 1] == 2 - 2
        assert m[0, 2] == 3 - 3
        assert m[1, 0] == 4 - 4
        assert m[1, 1] == 5 - 5
        assert m[1, 2] == 6 - 6
        assert m[2, 0] == 7 - 7
        assert m[2, 1] == 8 - 8
        assert m[2, 2] == 9 - 9
        assert m._shape == (3, 3)
        assert n._shape == (3, 3)
        # Matrix addition, different sizes...
        o = self.MatrixClass([[1, 2, 3]], default=0)
        with pytest.raises(ValueError):
            m -= o
        p = self.MatrixClass([[1], [2], [3]], default=0)
        with pytest.raises(ValueError):
            m -= p
        assert m[0, 0] == 1 - 1
        assert m[1, 1] == 5 - 5
        assert m[2, 2] == 9 - 9
        # Scalar addition
        s = 4
        n -= s
        assert n[0, 0] == 1 - s
        assert n[0, 1] == 2 - s
        assert n[0, 2] == 3 - s
        assert n[1, 0] == 4 - s
        assert n[1, 1] == 5 - s
        assert n[1, 2] == 6 - s
        assert n[2, 0] == 7 - s
        assert n[2, 1] == 8 - s
        assert n[2, 2] == 9 - s
        assert n._shape == (3, 3)

    def test__imul__(self):
        """Test *= / __imul__."""
        m = self._make_3x3_test_matrix()
        m *= 2
        assert m.aslist() == [[2, 4, 6], [8, 10, 12], [14, 16, 18]]

    def test__imatmul__(self):
        """Test *= / __imatmul__."""
        m = self._make_3x3_test_matrix()
        o = self._make_3x3_test_matrix()
        m @= o
        assert m.aslist() == [[30, 36, 42], [66, 81, 96], [102, 126, 150]]
        assert o.values() == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        incompatible = Matrix([], shape=(2, 3), default=2)
        with pytest.raises(ValueError):
            m @= incompatible
        with pytest.raises(ValueError):
            incompatible @= m
        assert m.aslist() == [[30, 36, 42], [66, 81, 96], [102, 126, 150]]
        assert incompatible.aslist() == [[2, 2, 2], [2, 2, 2]]


class TestSetters(CommonTestBase):

    MatrixClass = Matrix

    def test_cell_assignment(self):
        """Test single cell value assignments."""
        m = self._make_2x3_test_matrix()
        # 1, 2, 3
        # 4, 5, 6
        m[0, 0] = 99
        assert m[0, 0] == 99
        m[1, 1] = "x"
        assert m[1, 1] == "x"
        m[1, 2] = (1, 2, 3)
        assert m[1, 2] == (1, 2, 3)
        m[(1, 0)] = 10
        assert m[1, 0] == 10
        with pytest.raises(TypeError):
            m[9] = 0

    def test_cell_set(self):
        """Test single cell set() method."""
        m = self._make_2x3_test_matrix()
        m.set(0, 0, 99)
        assert m[0, 0] == 99
        m.set(1, 1, "x")
        assert m[1, 1] == "x"
        m.set(1, 2, (1, 2, 3))
        assert m[1, 2] == (1, 2, 3)
        m.set((1, 0), 10)
        assert m[1, 0] == 10
        m.set(1, 0, None)
        assert m[1, 0] is None
        with pytest.raises(TypeError):
            m.set(1, 0)  # No value provided
        with pytest.raises(TypeError):
            m.set((1, 0))  # No value provided

    def test_slice_assignment_matrix(self):
        """Test slice assignment with matrices."""
        m = self._make_2x3_test_matrix()
        t = Matrix([], (2, 3), default=1)
        m[:, :] = t
        assert m == t
        m = self._make_2x3_test_matrix()
        m[0, :] = t[0, :]
        assert m[0, 0] == 1
        assert m[0, 1] == 1
        assert m[0, 2] == 1
        assert m[1, 0] == 4
        assert m[1, 1] == 5
        assert m[1, 2] == 6
        m = self._make_2x3_test_matrix()
        m[:, 1] = Matrix([[1], [1]], default=1)
        assert m[0, 0] == 1
        assert m[0, 1] == 1
        assert m[0, 2] == 3
        assert m[1, 0] == 4
        assert m[1, 1] == 1
        assert m[1, 2] == 6
        with pytest.raises(ValueError):
            m[:, 1] = Matrix([], (0, 0), default=0)
        with pytest.raises(ValueError):
            m[:, 1] = t

    def test_slice_assignment_sequence(self):
        """Test slice assignment with sequences."""
        t = Matrix([], (2, 3), default=1)
        m = self._make_2x3_test_matrix()
        m[:, :] = [1, 1, 1, 1, 1, 1]
        assert m == t
        m = self._make_2x3_test_matrix()
        m[:, :] = [[1, 1, 1], [1, 1, 1]]
        assert m == t
        m = self._make_2x3_test_matrix()
        m[0, :] = 1, 1, 1
        m[1, :] = 2, 2, 2
        assert m[0, 0] == 1
        assert m[0, 1] == 1
        assert m[0, 2] == 1
        assert m[1, 0] == 2
        assert m[1, 1] == 2
        assert m[1, 2] == 2
        m = self._make_2x3_test_matrix()
        m[:, 1] = [(1, ), (1, )]
        assert m[0, 0] == 1
        assert m[0, 1] == 1
        assert m[0, 2] == 3
        assert m[1, 0] == 4
        assert m[1, 1] == 1
        assert m[1, 2] == 6
        with pytest.raises(TypeError):
            m[:, 1] = 1
        with pytest.raises(TypeError):
            m[0, :] = 1
        with pytest.raises(ValueError):
            m[:, 1] = []
        with pytest.raises(ValueError):
            m[:, 1] = [0, 1, 2, 3, 4, 5]
