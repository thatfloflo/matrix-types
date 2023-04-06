import pytest  # noqa: F401
from matrix_types import Matrix


class TestMatrixInitialisation:

    def test_init_from_seqseq(self):
        """Initialise with sequence of sequences."""
        Matrix([[1, 2, 3], [4, 5, 6]], default=0)
        Matrix([[1, 2, 3], [4, 5, 6]], shape=(2, 3), default=0)
        Matrix([[1, 2, 3], [4, 5, 6]], (2, 3), default=0)
        with pytest.raises(TypeError):
            Matrix([[1, 2, 3], [4, 5, 6]])
        with pytest.raises(TypeError):
            Matrix([[1, 2, 3], [4, 5, 6]], shape=(2, 3))
        with pytest.raises(TypeError):
            Matrix([[1, 2, 3], [4, 5, 6]], (2, 3))
        with pytest.raises(TypeError):
            Matrix([[1, 2, 3], [4, 5, 6]], (2, 3), 0)

    def test_init_from_matrix(self):
        """Initialise from existing Matrix."""
        m = Matrix([[1, 2, 3], [4, 5, 6]], default=0)
        Matrix(m)
        Matrix(m, default=-1)
        Matrix(m, shape=(3, 2), default=-1)
        Matrix(m, (3, 2), default=-1)

    def test_init_from_flat_sequence(self):
        """Initialise from a flat sequence."""
        Matrix([1, 2, 3, 4, 5, 6], shape=(2, 3), default=0)
        Matrix([1, 2, 3, 4, 5, 6], (2, 3), default=0)
        with pytest.raises(TypeError):
            Matrix([1, 2, 3, 4, 5, 6])
        with pytest.raises(TypeError):
            Matrix([1, 2, 3, 4, 5, 6], shape=(2, 3))
        with pytest.raises(TypeError):
            Matrix([1, 2, 3, 4, 5, 6], (2, 3))
        with pytest.raises(TypeError):
            Matrix([1, 2, 3, 4, 5, 6], default=0)


class TestMatrixGetters:

    def _make_2x3_test_matrix(self) -> Matrix:
        """Make a 2x3 test matrix."""
        return Matrix([[1, 2, 3], [4, 5, 6]], default=0)

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
        with pytest.raises(IndexError):
            m.get(0, 3)
        with pytest.raises(IndexError):
            m.get(2, 0)
        with pytest.raises(IndexError):
            m.get(0, -4)
        with pytest.raises(IndexError):
            m.get(-3, 0)

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
        with pytest.raises(IndexError):
            m[0, 3]
        with pytest.raises(IndexError):
            m[2, 0]
        with pytest.raises(IndexError):
            m[0, -4]
        with pytest.raises(IndexError):
            m[-3, 0]

    def test_getitem_missing_arg(self):
        """Test __getitem__ with missing argument."""
        m = self._make_2x3_test_matrix()
        with pytest.raises(TypeError):
            m[0]
        with pytest.raises(TypeError):
            m[0, ]
        with pytest.raises(TypeError):
            m[1:2:1]
        with pytest.raises(TypeError):
            m[None, None]

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


class TestMatrixShapes:

    def _make_2x3_test_matrix(self) -> Matrix:
        """Make a 2x3 test matrix."""
        return Matrix([[1, 2, 3], [4, 5, 6]], default=0)

    def _check_2x3_values(self, m: Matrix):
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 2
        assert m.get(0, 2) == 3
        assert m.get(1, 0) == 4
        assert m.get(1, 1) == 5
        assert m.get(1, 2) == 6

    def test_from_list_of_list(self):
        """Initialize Matrix from list of lists."""
        m = Matrix([[1, 2, 3], [4, 5, 6]], default=0)
        self._check_2x3_values(m)

    def test_from_tuple_of_tuples(self):
        """Initialize Matrix from tuple of tuples."""
        m = Matrix(((1, 2, 3), (4, 5, 6)), default=0)
        self._check_2x3_values(m)

    def test_from_flat_list(self):
        """Initialize Matrix from a flat list."""
        m = Matrix([1, 2, 3, 4, 5, 6], shape=(2, 3), default=0)
        self._check_2x3_values(m)

    def test_from_iterator(self):
        """Initialize Matrix from a iterator."""
        m = Matrix(range(1, 20), shape=(2, 3), default=0)
        self._check_2x3_values(m)
        print(m._data)
        with pytest.raises(IndexError):
            m.get(0, 3)
        with pytest.raises(IndexError):
            m.get(2, 0)

    def test_from_matrix(self):
        """Initialize from another Matrix."""
        m = Matrix((1, 2, 3, 4, 5, 6), shape=(2, 3), default=0)
        n = Matrix(m)
        assert m is not n
        assert m._shape == n._shape
        assert m._data == m._data

    def test_transpose(self):
        """Transpose x1 and check values, transpose x3 and check values."""
        m = self._make_2x3_test_matrix()
        m.transpose()
        assert m.get(0, 0) == 1
        assert m.get(1, 0) == 2
        assert m.get(2, 0) == 3
        assert m.get(0, 1) == 4
        assert m.get(1, 1) == 5
        assert m.get(2, 1) == 6
        m.transpose()  # Back to normal
        m.transpose().transpose()  # Should have no effect
        self._check_2x3_values(m)

    def test_resize_grow(self):
        """Resize->grow and check size and values."""
        m = self._make_2x3_test_matrix()
        m.resize(4, 4)
        self._check_2x3_values(m)
        assert m._shape == (4, 4)
        assert m.get(2, 0) == 0
        assert m.get(2, 1) == 0
        assert m.get(2, 1) == 0
        assert m.get(2, 2) == 0
        assert m.get(2, 3) == 0
        assert m.get(3, 0) == 0
        assert m.get(3, 1) == 0
        assert m.get(3, 2) == 0
        assert m.get(3, 3) == 0
        with pytest.raises(IndexError):
            m.get(4, 0)
        with pytest.raises(IndexError):
            m.get(0, 4)

    def test_resize_shrink(self):
        """Resize->shrink and check size and values."""
        m = self._make_2x3_test_matrix()
        m.resize(1, 1)
        assert m._shape == (1, 1)
        assert m.get(0, 0) == 1
        with pytest.raises(IndexError):
            m.get(1, 0)
        with pytest.raises(IndexError):
            m.get(0, 1)

    def test_resize_shrinkgrow(self):
        """Resize->shrink->grow and check size and values."""
        m = self._make_2x3_test_matrix()
        m.resize(1, 1)
        m.resize(2, 2)
        assert m._shape == (2, 2)
        assert m.get(0, 0) == 1
        assert m.get(1, 0) == 0
        assert m.get(0, 1) == 0
        assert m.get(1, 1) == 0
        with pytest.raises(IndexError):
            m.get(2, 0)
        with pytest.raises(IndexError):
            m.get(0, 2)

    def test_flip_default(self):
        """Flip by rows (without specifying 'by' arg)."""
        m = Matrix([[1, 1], [2, 2], [3, 3]], default=0)
        assert m._shape == (3, 2)
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 1
        assert m.get(1, 0) == 2
        assert m.get(1, 1) == 2
        assert m.get(2, 0) == 3
        assert m.get(2, 1) == 3
        m.flip()
        assert m._shape == (3, 2)
        assert m.get(0, 0) == 3
        assert m.get(0, 1) == 3
        assert m.get(1, 0) == 2
        assert m.get(1, 1) == 2
        assert m.get(2, 0) == 1
        assert m.get(2, 1) == 1

    def test_flip_by_row(self):
        """Flip by rows (without explicit 'by' arg)."""
        m = Matrix([[1, 1], [2, 2], [3, 3]], default=0)
        assert m._shape == (3, 2)
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 1
        assert m.get(1, 0) == 2
        assert m.get(1, 1) == 2
        assert m.get(2, 0) == 3
        assert m.get(2, 1) == 3
        m.flip(by="row")
        assert m._shape == (3, 2)
        assert m.get(0, 0) == 3
        assert m.get(0, 1) == 3
        assert m.get(1, 0) == 2
        assert m.get(1, 1) == 2
        assert m.get(2, 0) == 1
        assert m.get(2, 1) == 1

    def test_flip_by_col(self):
        """Flip by columns (with 'by' arg)."""
        m = Matrix([[1, 2, 3], [1, 2, 3]], default=0)
        assert m._shape == (2, 3)
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 2
        assert m.get(0, 2) == 3
        assert m.get(1, 0) == 1
        assert m.get(1, 1) == 2
        assert m.get(1, 2) == 3
        m.flip(by="col")
        assert m._shape == (2, 3)
        assert m.get(0, 0) == 3
        assert m.get(0, 1) == 2
        assert m.get(0, 2) == 1
        assert m.get(1, 0) == 3
        assert m.get(1, 1) == 2
        assert m.get(1, 2) == 1

    def test_flipv(self):
        """Test that flipv is the same as flip(by="row")."""
        m1 = Matrix([[1, 1], [2, 2], [3, 3]], default=0)
        m2 = Matrix([[1, 1], [2, 2], [3, 3]], default=0)
        m1.flip(by="row")
        m2.flipv()
        assert m1._data == m2._data
        assert m1._shape == m2._shape

    def test_fliph(self):
        """Test that fliph is the same as flip(by="col")."""
        m1 = Matrix([[1, 2, 3], [1, 2, 3]], default=0)
        m2 = Matrix([[1, 2, 3], [1, 2, 3]], default=0)
        m1.flip(by="col")
        m2.fliph()
        assert m1._data == m2._data
        assert m1._shape == m2._shape


class TestMatrixRowOperations:

    def _make_2x3_test_matrix(self) -> Matrix:
        """Make a 2x3 test matrix."""
        return Matrix([[1, 2, 3], [4, 5, 6]], default=0)

    def test_insertrow_start(self):
        """Insert a row at the beginning."""
        m = self._make_2x3_test_matrix()
        m.insertrow(0, [-1, -2, -3])
        assert m._shape == (3, 3)
        assert m.get(0, 0) == -1
        assert m.get(0, 1) == -2
        assert m.get(0, 2) == -3

    def test_insertrow_middle(self):
        """Insert a row at the middle."""
        m = self._make_2x3_test_matrix()
        m.insertrow(1, [-1, -2, -3])
        assert m._shape == (3, 3)
        assert m.get(1, 0) == -1
        assert m.get(1, 1) == -2
        assert m.get(1, 2) == -3

    def test_insertrow_end(self):
        """Insert a row at the end."""
        m = self._make_2x3_test_matrix()
        m.insertrow(2, [-1, -2, -3])
        assert m._shape == (3, 3)
        assert m.get(2, 0) == -1
        assert m.get(2, 1) == -2
        assert m.get(2, 2) == -3
        with pytest.raises(IndexError):
            m.get(3, 0)

    def test_insertrow_after_end(self):
        """Inser a row with index much past number of rows."""
        m = self._make_2x3_test_matrix()
        m.insertrow(100, [-1, -2, -3])
        assert m._shape == (3, 3)
        assert m.get(2, 0) == -1
        assert m.get(2, 1) == -2
        assert m.get(2, 2) == -3
        with pytest.raises(IndexError):
            m.get(3, 0)

    def test_prependrow(self):
        """Prepend a row."""
        m = self._make_2x3_test_matrix()
        m.prependrow([-1, -2, -3])
        assert m._shape == (3, 3)
        assert m.get(0, 0) == -1
        assert m.get(0, 1) == -2
        assert m.get(0, 2) == -3

    def test_appendrow(self):
        """Append a row."""
        m = self._make_2x3_test_matrix()
        m.appendrow([-1, -2, -3])
        assert m._shape == (3, 3)
        assert m.get(2, 0) == -1
        assert m.get(2, 1) == -2
        assert m.get(2, 2) == -3
        with pytest.raises(IndexError):
            m.get(3, 0)

    def test_swaprows(self):
        """Swap two rows."""
        m = Matrix([[1, 1], [2, 2], [3, 3], [4, 4]], default=0)
        m.swaprows(1, 3)
        assert m._shape == (4, 2)
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 1
        assert m.get(1, 0) == 4
        assert m.get(1, 1) == 4
        assert m.get(2, 0) == 3
        assert m.get(2, 1) == 3
        assert m.get(3, 0) == 2
        assert m.get(3, 1) == 2

    def test_swaprows_negative(self):
        """Swap two rows using negative indices."""
        m = Matrix([[1, 1], [2, 2], [3, 3], [4, 4]], default=0)
        m.swaprows(-3, -1)
        assert m._shape == (4, 2)
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 1
        assert m.get(1, 0) == 4
        assert m.get(1, 1) == 4
        assert m.get(2, 0) == 3
        assert m.get(2, 1) == 3
        assert m.get(3, 0) == 2
        assert m.get(3, 1) == 2

    def test_swaprows_out_of_range(self):
        """Attempt to swap rows out of range."""
        m = Matrix([[1, 1], [2, 2], [3, 3], [4, 4]], default=0)
        with pytest.raises(IndexError):
            m.swaprows(1, 4)

    def test_delrow(self):
        """Delete a row."""
        m = Matrix([[1, 1], [2, 2], [3, 3], [4, 4]], default=0)
        m.delrow(1)
        assert m._shape == (3, 2)
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 1
        assert m.get(1, 0) == 3
        assert m.get(1, 1) == 3
        assert m.get(2, 0) == 4
        assert m.get(2, 1) == 4
        with pytest.raises(IndexError):
            m.get(3, 0)

    def test_delrow_negative(self):
        """Delete a row using a negative index."""
        m = Matrix([[1, 1], [2, 2], [3, 3], [4, 4]], default=0)
        m.delrow(-3)
        assert m._shape == (3, 2)
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 1
        assert m.get(1, 0) == 3
        assert m.get(1, 1) == 3
        assert m.get(2, 0) == 4
        assert m.get(2, 1) == 4
        with pytest.raises(IndexError):
            m.get(3, 0)

    def test_delrow_out_of_range(self):
        """Attempt to delete a row out of range."""
        m = Matrix([[1, 1], [2, 2], [3, 3], [4, 4]], default=0)
        with pytest.raises(IndexError):
            m.delrow(4)
        with pytest.raises(IndexError):
            m.delrow(-5)
        assert m._shape == (4, 2)


class TestMatrixColumnOperations:

    def _make_2x3_test_matrix(self) -> Matrix:
        """Make a 2x3 test matrix."""
        return Matrix([[1, 2, 3], [4, 5, 6]], default=0)

    def test_insertcol_start(self):
        """Insert a column at the beginning."""
        m = self._make_2x3_test_matrix()
        m.insertcol(0, [-1, -2])
        assert m._shape == (2, 4)
        assert m.get(0, 0) == -1
        assert m.get(0, 1) == 1
        assert m.get(0, 2) == 2
        assert m.get(0, 3) == 3
        assert m.get(1, 0) == -2
        assert m.get(1, 1) == 4
        assert m.get(1, 2) == 5
        assert m.get(1, 3) == 6

    def test_insertcol_middle(self):
        """Insert a column at the middle."""
        m = self._make_2x3_test_matrix()
        m.insertcol(1, [-1, -2])
        assert m._shape == (2, 4)
        assert m.get(0, 1) == -1
        assert m.get(1, 1) == -2

    def test_insertcol_end(self):
        """Insert a column at the end."""
        m = self._make_2x3_test_matrix()
        m.insertcol(3, [-1, -2])
        assert m._shape == (2, 4)
        assert m.get(0, 3) == -1
        assert m.get(1, 3) == -2
        with pytest.raises(IndexError):
            m.get(0, 4)

    def test_insertcol_after_end(self):
        """Insert a column with index much past number of columns."""
        m = self._make_2x3_test_matrix()
        m.insertcol(23, [-1, -2])
        assert m._shape == (2, 4)
        assert m.get(0, 3) == -1
        assert m.get(1, 3) == -2
        with pytest.raises(IndexError):
            m.get(0, 4)

    def test_prependcol(self):
        """Prepend a col."""
        m = self._make_2x3_test_matrix()
        m.prependcol([-1, -2])
        assert m._shape == (2, 4)
        assert m.get(0, 0) == -1
        assert m.get(1, 0) == -2

    def test_appendcol(self):
        """Append a column."""
        m = self._make_2x3_test_matrix()
        m.appendcol([-1, -2])
        assert m._shape == (2, 4)
        assert m.get(0, 3) == -1
        assert m.get(1, 3) == -2
        with pytest.raises(IndexError):
            m.get(0, 4)

    def test_swapcols(self):
        """Swap two columns."""
        m = Matrix([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]], default=0)
        m.swapcols(1, 3)
        assert m._shape == (3, 4)
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 4
        assert m.get(1, 1) == 4
        assert m.get(2, 1) == 4
        assert m.get(1, 2) == 3
        assert m.get(0, 3) == 2
        assert m.get(1, 3) == 2
        assert m.get(2, 3) == 2
        assert m.get(2, 3) == 2

    def test_swapcols_negative(self):
        """Swap two columns using negative indices."""
        m = Matrix([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]], default=0)
        m.swapcols(-1, -3)
        assert m._shape == (3, 4)
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 4
        assert m.get(1, 1) == 4
        assert m.get(2, 1) == 4
        assert m.get(1, 2) == 3
        assert m.get(0, 3) == 2
        assert m.get(1, 3) == 2
        assert m.get(2, 3) == 2
        assert m.get(2, 3) == 2

    def test_swapcols_out_of_range(self):
        """Attempt to swap columns out of range."""
        m = Matrix([[1, 1], [2, 2], [3, 3], [4, 4]], default=0)
        with pytest.raises(IndexError):
            m.swapcols(1, 4)

    def test_delcol(self):
        """Delete a column."""
        m = Matrix([[1, 2, 3, 4], [1, 2, 3, 4]], default=0)
        m.delcol(1)
        assert m._shape == (2, 3)
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 3
        assert m.get(0, 2) == 4
        assert m.get(1, 0) == 1
        assert m.get(1, 1) == 3
        assert m.get(1, 2) == 4
        with pytest.raises(IndexError):
            m.get(0, 3)

    def test_delcol_negative(self):
        """Delete a column using a negative index."""
        m = Matrix([[1, 2, 3, 4], [1, 2, 3, 4]], default=0)
        m.delcol(-3)
        assert m._shape == (2, 3)
        assert m.get(0, 0) == 1
        assert m.get(0, 1) == 3
        assert m.get(0, 2) == 4
        assert m.get(1, 0) == 1
        assert m.get(1, 1) == 3
        assert m.get(1, 2) == 4
        with pytest.raises(IndexError):
            m.get(0, 3)

    def test_delcol_out_of_range(self):
        """Attempt to delete a column out of range."""
        m = Matrix([[1, 2, 3, 4], [1, 2, 3, 4]], default=0)
        with pytest.raises(IndexError):
            m.delcol(4)
        with pytest.raises(IndexError):
            m.delcol(-5)
        assert m._shape == (2, 4)


class TestMatrixDataAccess:

    def _make_3x3_test_matrix(self) -> Matrix:
        """Make a 3x3 test matrix."""
        return Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], default=0)

    @pytest.mark.skip("Not yet implemented")
    def test_submatrix(self):
        """Test making submatrices."""
        m = self._make_3x3_test_matrix()
        t = m.submatrix((0, 1), (0, 1, 2))
        assert t._shape == (2, 3)
        assert t.get(0, 0) == 1
        assert t.get(0, 1) == 2
        assert t.get(0, 2) == 3
        assert t.get(1, 0) == 4
        assert t.get(1, 1) == 5
        assert t.get(1, 2) == 6
        with pytest.raises(IndexError):
            t.get(2, 0)
        t = m.submatrix((1, ), (1, ))
        assert t._shape == (1, 1)
        assert t.get(0, 0) == 5
        with pytest.raises(IndexError):
            t.get(0, 1)
        with pytest.raises(IndexError):
            t.get(1, 0)
        assert m._shape == (3, 3)

    def test_flatten_by_default(self):
        """Test flattening Matrix data to list with by=default."""
        m = self._make_3x3_test_matrix()
        t = m.flatten()
        assert isinstance(t, list)
        assert all(isinstance(x, int) for x in t)
        assert len(t) == m._shape[0] * m._shape[1]
        assert t == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_flatten_by_row(self):
        """Test flattening Matrix data to list with by="row"."""
        m = self._make_3x3_test_matrix()
        t = m.flatten(by="row")
        assert isinstance(t, list)
        assert all(isinstance(x, int) for x in t)
        assert len(t) == m._shape[0] * m._shape[1]
        assert t == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_flatten_by_column(self):
        """Test flattening Matrix data to list with by="col"."""
        m = self._make_3x3_test_matrix()
        t = m.flatten(by="col")
        assert isinstance(t, list)
        assert all(isinstance(x, int) for x in t)
        assert len(t) == m._shape[0] * m._shape[1]
        assert t == [1, 4, 7, 2, 5, 8, 3, 6, 9]

    def test_aslist_by_default(self):
        """Test fetching Matrix data as list of lists with by=default."""
        m = self._make_3x3_test_matrix()
        t = m.aslist()
        assert isinstance(t, list)
        assert all(isinstance(x, list) for x in t)
        assert len(t) == m._shape[0]
        assert all(len(x) == m._shape[1] for x in t)
        assert t == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def test_aslist_by_row(self):
        """Test fetching Matrix data as list of lists with by="row."""
        m = self._make_3x3_test_matrix()
        t = m.aslist(by="row")
        assert isinstance(t, list)
        assert all(isinstance(x, list) for x in t)
        assert len(t) == m._shape[0]
        assert all(len(x) == m._shape[1] for x in t)
        assert t == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def test_aslist_by_column(self):
        """Test fetching Matrix data as list of lists with by="col."""
        m = self._make_3x3_test_matrix()
        t = m.aslist(by="col")
        assert isinstance(t, list)
        assert all(isinstance(x, list) for x in t)
        assert len(t) == m._shape[1]
        assert all(len(x) == m._shape[0] for x in t)
        assert t == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

    def test_asdict(self):
        """Test fetching Matrix data as dict."""
        m = self._make_3x3_test_matrix()
        t = m.asdict()
        assert len(t) == m._shape[0] * m._shape[1]
        assert t == {
            (0, 0): 1,
            (0, 1): 2,
            (0, 2): 3,
            (1, 0): 4,
            (1, 1): 5,
            (1, 2): 6,
            (2, 0): 7,
            (2, 1): 8,
            (2, 2): 9,
        }


class TestMatrixOperations:

    def _make_3x3_test_matrix(self) -> Matrix:
        """Make a 3x3 test matrix."""
        return Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], default=0)

    def test_imatadd(self):
        """Test in-situ matrix addition."""
        m = self._make_3x3_test_matrix()
        o = self._make_3x3_test_matrix()
        m.imatadd(o)
        assert m.flatten() == [2, 4, 6, 8, 10, 12, 14, 16, 18]
        assert o.flatten() == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_matadd(self):
        """Test regular matrix addition."""
        m = self._make_3x3_test_matrix()
        o = self._make_3x3_test_matrix()
        t = m.matadd(o)
        assert t.flatten() == [2, 4, 6, 8, 10, 12, 14, 16, 18]
        assert m.flatten() == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert o.flatten() == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_imatsub(self):
        """Test in-situ matrix subtraction."""
        m = self._make_3x3_test_matrix()
        o = self._make_3x3_test_matrix()
        m.imatsub(o)
        assert m.flatten() == [0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert o.flatten() == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_matsub(self):
        """Test regular matrix subtraction."""
        m = self._make_3x3_test_matrix()
        o = self._make_3x3_test_matrix()
        t = m.matsub(o)
        assert t.flatten() == [0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert m.flatten() == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert o.flatten() == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_imatmul(self):
        """Test in-situ matrix multiplication."""
        m = self._make_3x3_test_matrix()
        o = self._make_3x3_test_matrix()
        m.imatmul(o)
        assert m.aslist() == [[30, 36, 42], [66, 81, 96], [102, 126, 150]]
        assert o.flatten() == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        incompatible = Matrix([], shape=(2, 3), default=0)
        with pytest.raises(ValueError):
            m.imatmul(incompatible)
        with pytest.raises(ValueError):
            incompatible.imatmul(m)
        assert m.aslist() == [[30, 36, 42], [66, 81, 96], [102, 126, 150]]

    def test_matmul(self):
        """Test regular matrix multiplication."""
        m = self._make_3x3_test_matrix()
        o = self._make_3x3_test_matrix()
        t = m.matmul(o)
        assert t.aslist() == [[30, 36, 42], [66, 81, 96], [102, 126, 150]]
        assert m.flatten() == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert o.flatten() == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        incompatible = Matrix([], shape=(2, 3), default=0)
        with pytest.raises(ValueError):
            m.matmul(incompatible)
        with pytest.raises(ValueError):
            incompatible.matmul(m)
        assert m.flatten() == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_iscaladd(self):
        """Test in-situ scalar addition."""
        m = self._make_3x3_test_matrix()
        m.iscaladd(2)
        assert m.aslist() == [[3, 4, 5], [6, 7, 8], [9, 10, 11]]

    def test_scaladd(self):
        """Test regular scalar addition."""
        m = self._make_3x3_test_matrix()
        t = m.scaladd(2)
        assert t.aslist() == [[3, 4, 5], [6, 7, 8], [9, 10, 11]]
        assert m.aslist() == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def test_iscalsub(self):
        """Test in-situ scalar subtraction."""
        m = self._make_3x3_test_matrix()
        m.iscalsub(2)
        assert m.aslist() == [[-1, 0, 1], [2, 3, 4], [5, 6, 7]]

    def test_scalsub(self):
        """Test regular scalar subtraction."""
        m = self._make_3x3_test_matrix()
        t = m.scalsub(2)
        assert t.aslist() == [[-1, 0, 1], [2, 3, 4], [5, 6, 7]]
        assert m.aslist() == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def test_iscalmul(self):
        """Test in-situ scalar multiplication."""
        m = self._make_3x3_test_matrix()
        m.iscalmul(2)
        assert m.aslist() == [[2, 4, 6], [8, 10, 12], [14, 16, 18]]

    def test_scalmul(self):
        """Test regular scalar subtraction."""
        m = self._make_3x3_test_matrix()
        t = m.scalmul(2)
        assert t.aslist() == [[2, 4, 6], [8, 10, 12], [14, 16, 18]]
        assert m.aslist() == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def test_foreach(self):
        """Test Matrix.foreach()."""
        m = self._make_3x3_test_matrix()
        collection = []
        m.foreach(lambda a: collection.append(a**2))
        assert collection == [1, 4, 9, 16, 25, 36, 49, 64, 81]
        assert m.aslist() == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def test_map(self):
        """Test Matrix.map()."""
        m = self._make_3x3_test_matrix()
        m.map(lambda a: a**2)
        assert m.aslist() == [[1, 4, 9], [16, 25, 36], [49, 64, 81]]


class TestMatrixDunders:

    def _make_3x3_test_matrix(self) -> Matrix:
        """Make a 3x3 test matrix."""
        return Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], default=0)

    def test__str__(self):
        """Test str() / __str__."""
        m = self._make_3x3_test_matrix()
        t = str(m)
        print(t)
        assert isinstance(t, str)
        assert "1" in t
        assert "2" in t
        assert "3" in t
        assert "4" in t
        assert "5" in t
        assert "6" in t
        assert "7" in t
        assert "8" in t
        assert "9" in t

    def test__repr__(self):
        """Test repr() / __repr__."""
        m = self._make_3x3_test_matrix()
        t = eval(f"{m!r}")
        assert isinstance(t, Matrix)
        assert t._shape == (3, 3)
        assert t.flatten() == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test__eq__(self):
        """Test == / __eq__."""
        m = self._make_3x3_test_matrix()
        same = self._make_3x3_test_matrix()
        diff1 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 10]], default=0)
        diff2 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]], default=0)
        assert m is m
        assert m == m
        assert m is not same
        assert m == same
        assert not (m == diff1)
        assert not (m == diff2)

    def test__bool__(self):
        """Test bool() / __bool__."""
        truthy1 = self._make_3x3_test_matrix()
        truthy2 = Matrix([[True, True], [True, True]], default=None)
        truthy3 = Matrix([[False, False], [False, False]], default=None)
        truthy4 = Matrix([[None, None], [None, None]], default=0)
        assert bool(truthy1) is True
        assert bool(truthy2) is True
        assert bool(truthy3) is True
        assert bool(truthy4) is True
        falsy1 = Matrix([], shape=(3, 3), default=0)
        falsy2 = Matrix([[0, 0, 0], [0, 0, 0]], default=0)
        falsy3 = Matrix([[True, True], [True, True]], default=True)
        assert bool(falsy1) is False
        assert bool(falsy2) is False
        assert bool(falsy3) is False

    def test__len__(self):
        """Test len() / __len__."""
        assert len(self._make_3x3_test_matrix()) == 3*3
        assert len(Matrix([], shape=(123, 5), default=0)) == 123*5
        assert len(Matrix([], shape=(0, 0), default=0)) == 0
        assert len(Matrix([], shape=(10, 0), default=0)) == 0
        assert len(Matrix([], shape=(0, 10), default=0)) == 0

    def test__contains__(self):
        """Test in / __contains__."""
        m = self._make_3x3_test_matrix()
        assert 1 in m
        assert 2 in m
        assert 3 in m
        assert 4 in m
        assert 5 in m
        assert 6 in m
        assert 7 in m
        assert 8 in m
        assert 9 in m
        assert 0 not in m
        assert 10 not in m

    @pytest.mark.skip("Test to be written, mirror matadd/scaladd")
    def test__add__(self):
        """Test + / __add__."""

    @pytest.mark.skip("Test to be written, mirror imatadd/iscaladd")
    def test__iadd__(self):
        """Test += / __iadd__."""

    @pytest.mark.skip("Test to be written, mirror matsub/scalsub")
    def test__sub__(self):
        """Test - / __sub__."""

    @pytest.mark.skip("Test to be written, mirror imatsub/iscalsub")
    def test__isub__(self):
        """Test -= / __isub__."""

    @pytest.mark.skip("Test to be written, mirror scalmul")
    def test__mul__(self):
        """Test * / __mul__."""

    @pytest.mark.skip("Test to be written, mirror iscalmul")
    def test__imul__(self):
        """Test *= / __imul__."""

    @pytest.mark.skip("Test to be written, mirror matmul")
    def test__matmul__(self):
        """Test * / __matmul__."""

    @pytest.mark.skip("Test to be written, mirror imatmul")
    def test__imatmul__(self):
        """Test *= / __imatmul__."""
