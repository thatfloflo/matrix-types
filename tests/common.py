import pytest  # noqa: F401
from typing import ClassVar
from matrix_types._base import MatrixABC
from matrix_types import Matrix, FrozenMatrix


class CommonTestBase:

    MatrixClass: ClassVar[MatrixABC]

    def _make_2x3_test_matrix(self) -> Matrix:
        """Make a 2x3 test matrix."""
        return self.MatrixClass([[1, 2, 3], [4, 5, 6]], default=0)


class CommonInitTests(CommonTestBase):

    def test_init_from_seqseq(self):
        """Initialise with sequence of sequences."""
        self.MatrixClass([[1, 2, 3], [4, 5, 6]], default=0)
        self.MatrixClass([[1, 2, 3], [4, 5, 6]], shape=(2, 3), default=0)
        self.MatrixClass([[1, 2, 3], [4, 5, 6]], (2, 3), default=0)
        with pytest.raises(TypeError):
            self.MatrixClass([[1, 2, 3], [4, 5, 6]])
        with pytest.raises(TypeError):
            self.MatrixClass([[1, 2, 3], [4, 5, 6]], shape=(2, 3))
        with pytest.raises(TypeError):
            self.MatrixClass([[1, 2, 3], [4, 5, 6]], (2, 3))
        with pytest.raises(TypeError):
            self.MatrixClass([[1, 2, 3], [4, 5, 6]], (2, 3), 0)

    def test_init_from_matrix(self):
        """Initialise from existing Matrix."""
        m = Matrix([[1, 2, 3], [4, 5, 6]], default=0)
        self.MatrixClass(m)
        self.MatrixClass(m, default=-1)
        self.MatrixClass(m, shape=(3, 2), default=-1)
        self.MatrixClass(m, (3, 2), default=-1)

    def test_init_from_frozenmatrix(self):
        """Initialise from existing FrozenMatrix."""
        m = FrozenMatrix([[1, 2, 3], [4, 5, 6]], default=0)
        self.MatrixClass(m)
        self.MatrixClass(m, default=-1)
        self.MatrixClass(m, shape=(3, 2), default=-1)
        self.MatrixClass(m, (3, 2), default=-1)

    def init_from_flat_sequence(self):
        """Initialise from a flat sequence."""
        self.MatrixClass([1, 2, 3, 4, 5, 6], shape=(2, 3), default=0)
        self.MatrixClass([1, 2, 3, 4, 5, 6], (2, 3), default=0)
        with pytest.raises(TypeError):
            self.MatrixClass([1, 2, 3, 4, 5, 6])
        with pytest.raises(TypeError):
            self.MatrixClass([1, 2, 3, 4, 5, 6], shape=(2, 3))
        with pytest.raises(TypeError):
            self.MatrixClass([1, 2, 3, 4, 5, 6], (2, 3))
        with pytest.raises(TypeError):
            self.MatrixClass([1, 2, 3, 4, 5, 6], default=0)


class CommonGetterTests(CommonTestBase):

    def test_get_indices(self):
        """Test get() with (positive) indeces."""
        m = self._make_2x3_test_matrix()
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 2
        assert m.get(0, 2) == 3
        assert m.get(1, 0) == 4
        assert m.get(1, 1) == 5
        assert m.get(1, 2) == 6

    def test_get_indeces_negative(self):
        """Test get() with negative indices."""
        m = self._make_2x3_test_matrix()
        assert m.get(-2, -3) == 1
        assert m.get(-2, -2) == 2
        assert m.get(-2, -1) == 3
        assert m.get(-1, -3) == 4
        assert m.get(-1, -2) == 5
        assert m.get(-1, -1) == 6

    def test_get_indeces_out_of_range(self):
        """Test get() with indeces out of range."""
        m = self._make_2x3_test_matrix()
        with pytest.raises(IndexError) as excinfo:
            m.get(0, 3)
        assert "range" in str(excinfo.value)
        with pytest.raises(IndexError) as excinfo:
            m.get(2, 0)
        assert "range" in str(excinfo.value)
        with pytest.raises(IndexError) as excinfo:
            m.get(0, -4)
        assert "range" in str(excinfo.value)
        with pytest.raises(IndexError) as excinfo:
            m.get(-3, 0)
        assert "range" in str(excinfo.value)

    def test_getitem_indeces(self):
        """Test __getitem__ with (positive) indeces."""
        m = self._make_2x3_test_matrix()
        assert m[0, 0] == 1
        assert m[0, 1] == 2
        assert m[0, 2] == 3
        assert m[1, 0] == 4
        assert m[1, 1] == 5
        assert m[1, 2] == 6

    def test_getitem_indeces_negative(self):
        """Test __getitem__ with (positive) indeces."""
        m = self._make_2x3_test_matrix()
        assert m[-2, -3] == 1
        assert m[-2, -2] == 2
        assert m[-2, -1] == 3
        assert m[-1, -3] == 4
        assert m[-1, -2] == 5
        assert m[-1, -1] == 6

    def test_getitem_indeces_out_of_range(self):
        """Test __getitem__ with indeces out of range."""
        m = self._make_2x3_test_matrix()
        with pytest.raises(IndexError) as excinfo:
            m[0, 3]
        assert "range" in str(excinfo.value)
        with pytest.raises(IndexError) as excinfo:
            m[2, 0]
        assert "range" in str(excinfo.value)
        with pytest.raises(IndexError) as excinfo:
            m[0, -4]
        assert "range" in str(excinfo.value)
        with pytest.raises(IndexError) as excinfo:
            m[-3, 0]
        assert "range" in str(excinfo.value)

    def test_getitem_missing_arg(self):
        """Test __getitem__ with missing argument."""
        m = self._make_2x3_test_matrix()
        with pytest.raises(TypeError) as excinfo:
            m[0]
        assert "tuple" in str(excinfo.value)
        with pytest.raises(TypeError) as excinfo:
            m[0, ]
        assert "tuple" in str(excinfo.value)
        with pytest.raises(TypeError) as excinfo:
            m[1:2:1]
        assert "tuple" in str(excinfo.value)
        with pytest.raises(TypeError) as excinfo:
            m[None, None]
        assert "tuple" in str(excinfo.value)

    def test_getitem_slices(self):
        """Test __getitem__ with slices."""
        m = self._make_2x3_test_matrix()
        assert m[0:, 0:].aslist() == [[1, 2, 3], [4, 5, 6]]
        assert m[1:, 1:].aslist() == [[5, 6]]
        assert m[0:2, 0:1].aslist() == [[1], [4]]
        assert m[2:2, 1:1]._shape == (0, 0)
        assert m[::2, ::1].aslist() == [[1, 2, 3]]
        assert m[::1, ::2].aslist() == [[1, 3], [4, 6]]

    def test_getitem_slices_negative(self):
        """Test __getitem__ with negative."""
        m = self._make_2x3_test_matrix()
        #     0  1  2
        #   ┌         ┐
        # 0 │ 1  2  3 │
        # 1 │ 4  5  6 │
        #   └         ┘
        assert m[-2:, -3:].aslist() == [[1, 2, 3], [4, 5, 6]]
        assert m[-1:, -2:].aslist() == [[5, 6]]
        assert m[0:2, 0:-2].aslist() == [[1], [4]]
        assert m[0:-1, -3:].aslist() == [[1, 2, 3]]
        assert m[-2:-2, -1:-1]._shape == (0, 0)
        assert m[::2, ::1].aslist() == [[1, 2, 3]]
        assert m[::1, ::2].aslist() == [[1, 3], [4, 6]]


class CommonShapeTests(CommonTestBase):

    def _check_2x3_values(self, m: Matrix):
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 2
        assert m.get(0, 2) == 3
        assert m.get(1, 0) == 4
        assert m.get(1, 1) == 5
        assert m.get(1, 2) == 6

    def test_from_list_of_list(self):
        """Initialize Matrix from list of lists."""
        m = self.MatrixClass([[1, 2, 3], [4, 5, 6]], default=0)
        self._check_2x3_values(m)

    def test_from_tuple_of_tuples(self):
        """Initialize Matrix from tuple of tuples."""
        m = self.MatrixClass(((1, 2, 3), (4, 5, 6)), default=0)
        self._check_2x3_values(m)

    def test_from_flat_list(self):
        """Initialize Matrix from a flat list."""
        m = self.MatrixClass([1, 2, 3, 4, 5, 6], shape=(2, 3), default=0)
        self._check_2x3_values(m)

    def test_from_iterator(self):
        """Initialize Matrix from a iterator."""
        m = self.MatrixClass(range(1, 20), shape=(2, 3), default=0)
        self._check_2x3_values(m)
        print(m._data)
        with pytest.raises(IndexError):
            m.get(0, 3)
        with pytest.raises(IndexError):
            m.get(2, 0)

    def test_from_matrix(self):
        """Initialize from another Matrix."""
        m = Matrix((1, 2, 3, 4, 5, 6), shape=(2, 3), default=0)
        n = self.MatrixClass(m)
        assert m is not n
        assert m._shape == n._shape
        assert m._data == m._data

    def test_from_frozenmatrix(self):
        """Initialize from another FrozenMatrix."""
        m = FrozenMatrix((1, 2, 3, 4, 5, 6), shape=(2, 3), default=0)
        n = self.MatrixClass(m)
        assert m is not n
        assert m._shape == n._shape
        assert m._data == m._data

    def test_transpose(self):
        """Transpose x1 and check values, transpose x3 and check values."""
        m = self._make_2x3_test_matrix()
        t = m.transpose()
        assert t.get(0, 0) == 1
        assert t.get(1, 0) == 2
        assert t.get(2, 0) == 3
        assert t.get(0, 1) == 4
        assert t.get(1, 1) == 5
        assert t.get(2, 1) == 6
        t = t.transpose()  # Back to normal
        t = t.transpose().transpose()  # Should have no effect
        self._check_2x3_values(t)

    def test_resize_grow(self):
        """Resize->grow and check size and values."""
        m = self._make_2x3_test_matrix()
        t = m.resize(4, 4)
        self._check_2x3_values(t)
        assert t._shape == (4, 4)
        assert t.get(2, 0) == 0
        assert t.get(2, 1) == 0
        assert t.get(2, 1) == 0
        assert t.get(2, 2) == 0
        assert t.get(2, 3) == 0
        assert t.get(3, 0) == 0
        assert t.get(3, 1) == 0
        assert t.get(3, 2) == 0
        assert t.get(3, 3) == 0
        with pytest.raises(IndexError):
            t.get(4, 0)
        with pytest.raises(IndexError):
            t.get(0, 4)

    def test_resize_shrink(self):
        """Resize->shrink and check size and values."""
        m = self._make_2x3_test_matrix()
        t = m.resize(1, 1)
        assert t._shape == (1, 1)
        assert t.get(0, 0) == 1
        with pytest.raises(IndexError):
            t.get(1, 0)
        with pytest.raises(IndexError):
            t.get(0, 1)

    def test_resize_shrinkgrow(self):
        """Resize->shrink->grow and check size and values."""
        m = self._make_2x3_test_matrix()
        t = m.resize(1, 1)
        t = t.resize(2, 2)
        assert t._shape == (2, 2)
        assert t.get(0, 0) == 1
        assert t.get(1, 0) == 0
        assert t.get(0, 1) == 0
        assert t.get(1, 1) == 0
        with pytest.raises(IndexError):
            t.get(2, 0)
        with pytest.raises(IndexError):
            t.get(0, 2)

    def test_flip_default(self):
        """Flip by rows (without specifying 'by' arg)."""
        m = self.MatrixClass([[1, 1], [2, 2], [3, 3]], default=0)
        assert m._shape == (3, 2)
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 1
        assert m.get(1, 0) == 2
        assert m.get(1, 1) == 2
        assert m.get(2, 0) == 3
        assert m.get(2, 1) == 3
        t = m.flip()
        assert t._shape == (3, 2)
        assert t.get(0, 0) == 3
        assert t.get(0, 1) == 3
        assert t.get(1, 0) == 2
        assert t.get(1, 1) == 2
        assert t.get(2, 0) == 1
        assert t.get(2, 1) == 1

    def test_flip_by_row(self):
        """Flip by rows (without explicit 'by' arg)."""
        m = self.MatrixClass([[1, 1], [2, 2], [3, 3]], default=0)
        assert m._shape == (3, 2)
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 1
        assert m.get(1, 0) == 2
        assert m.get(1, 1) == 2
        assert m.get(2, 0) == 3
        assert m.get(2, 1) == 3
        t = m.flip(by="row")
        assert t._shape == (3, 2)
        assert t.get(0, 0) == 3
        assert t.get(0, 1) == 3
        assert t.get(1, 0) == 2
        assert t.get(1, 1) == 2
        assert t.get(2, 0) == 1
        assert t.get(2, 1) == 1

    def test_flip_by_col(self):
        """Flip by columns (with 'by' arg)."""
        m = self.MatrixClass([[1, 2, 3], [1, 2, 3]], default=0)
        assert m._shape == (2, 3)
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 2
        assert m.get(0, 2) == 3
        assert m.get(1, 0) == 1
        assert m.get(1, 1) == 2
        assert m.get(1, 2) == 3
        t = m.flip(by="col")
        assert t._shape == (2, 3)
        assert t.get(0, 0) == 3
        assert t.get(0, 1) == 2
        assert t.get(0, 2) == 1
        assert t.get(1, 0) == 3
        assert t.get(1, 1) == 2
        assert t.get(1, 2) == 1

    def test_flipv(self):
        """Test that flipv is the same as flip(by="row")."""
        m1 = self.MatrixClass([[1, 1], [2, 2], [3, 3]], default=0)
        m2 = self.MatrixClass([[1, 1], [2, 2], [3, 3]], default=0)
        t1 =m1.flip(by="row")
        t2 = m2.flipv()
        assert t1._data == t2._data
        assert t1._shape == t2._shape

    def test_fliph(self):
        """Test that fliph is the same as flip(by="col")."""
        m1 = self.MatrixClass([[1, 2, 3], [1, 2, 3]], default=0)
        m2 = self.MatrixClass([[1, 2, 3], [1, 2, 3]], default=0)
        t1 = m1.flip(by="col")
        t2 = m2.fliph()
        assert t1._data == t2._data
        assert t1._shape == t2._shape
