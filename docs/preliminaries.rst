Preliminaries
=============

Matrices as a data type
-----------------------

Matrices are familiar to most programmers from maths, at least vaguely, but
even beyond strictly mathematical needs they are a useful data type which is
often encountered where computations or the organisation of data for other
tasks requires a two-dimensional structure, for example with dynamic
programming algorithms, image manipulation, etc. It is best to think of a
matrix as a two-dimensional table, with numbered rows and columns uniquely
identifying each cell of the table.

For example, the matrix below has 3 rows (numbered 0-2) and 5 columns
(numbered 0-4), we call this a 3x5 matrix:

:math:`\begin{bmatrix}(0,0) & (0,1) & (0,2) & (0,3) & (0,4)\\(0,1) & (1,1) & (1,2) & (1,3) & (1,4)\\(0,2) & (2,1) & (2,2) & (2,3) & (2,4)\end{bmatrix}`

We can think of this matrix as a *table*, with the header column and header row
showing the *row* and *column* indices, respectively:

+-------+-------+-------+-------+-------+-------+
|       | **0** | **1** | **2** | **3** | **4** |
+-------+-------+-------+-------+-------+-------+
| **0** |  0, 0 |  0, 1 |  0, 2 |  0, 3 |  0, 4 |
+-------+-------+-------+-------+-------+-------+
| **1** |  1, 0 |  1, 1 |  1, 2 |  1, 3 |  1, 4 |
+-------+-------+-------+-------+-------+-------+
| **2** |  2, 0 |  2, 1 |  2, 2 |  2, 3 |  2, 4 |
+-------+-------+-------+-------+-------+-------+

The 3x5 matrix above has 15 cells, and each cell can be addressed specifically
by a combination of its *row index* and its *column index*. For example, the
cell shown with the value "1, 3" has the row index *1* and the column index
*3*, so we can access the individual value with the coordinates *(1, 3)*.
We can also iterate through the rows or columns of the matrix by increasing the
row or column index, or both, until we have reached all the desired cells.

Of course, while we are mostly familiar with matrices holding numeric data,
the data type in the cells could be anything. For instance, for a colour image
the cells might each hold a RGB triplet (or an RGBa quadruplet with
an alpha channel for transparency), for ASCII Art or the screen of a Terminal
they might hold ASCII or Unicode characters, but depending on need they can
in principle hold any type of data in their cells, e.g. numbers, strings,
lists, tuples, sets, dicts, or arbitrary objects -- even other matrices.


Why you should use a specific matrix data type
----------------------------------------------

Unfortunately, the Python standard library does not provide a built-in
data type for matrices, so that they are commonly emulated as lists of lists,
tuples of tuples, and similar. For example, a common way of representing the
3x5 matrix above in Python would be as a list of lists such as ::

    [
        ["0, 0", "0, 1", "0, 2", "0, 3", "0, 4"],
        ["1, 0", "1, 1", "1, 2", "1, 3", "1, 4"],
        ["2, 0", "2, 1", "2, 2", "2, 3", "2, 4"],
    ]

This is often convenient because we already have all the pieces we need in
Python's standard library, but it also makes some things more cumbersome than
the should be. For example, to find the dimensions of such a matrix, we have
to *know* that it is implemented a sequence of sequences, and then minimally
check the length of the outer sequence (to get the number of rows) and the
length of at least one of the inner sequences (to get the number of columns).
We could of course package this into a nice little function, for example ::

    def get_shape(matrix: Sequence[Sequence[Any]]) -> tuple[int, int]:
        rows = len(matrix)
        cols = len(matrix[0])
        return (rows, cols)

But what if our matrix has zero rows (yes, 0x0, *n*\ x0 and 0x\ *n* matrices are
things that can be useful, they're not necessarily a mishap)? If we pass a 0x0
matrix to :py:func:`get_shape()` it raise an :py:obj:`IndexError`, because
we're trying to access :code:`matrix[0]` but there is no 0-index item in the
matrix! Of course, we could just agree that we should always represent the
0x0 matrix as :code:`[[]]` and never as just :code:`[]`, but this is
another ad-hoc convention everyone reading, using or modifying our code must
know and adhere to, and it makes it difficult to distinguish a 0x0 matrix from
a 1x0 matrix (which we might not care about at present, but maybe someone has
a nifty idea in the future that then breaks everything).

Now consider also what happens when we carry out some operation on the rows of
this matrix. The lists representing each row are of course mutable structures,
and so items can be added or removed from them. What if we end up with a row
that is one shorter or longer than the others? Should we check that all the
lists representing the rows have an equal length after every operation carried
out on them, or just trust that nobody will do anything that leaves them with
inconsistent lengths? If we repair them, how do we know what to fill in as the
'default' value (*0* or :py:obj:`None` may not always be appropriate!).

For all these reasons, and many more, when we want to actually work with data
that is best represented in the form of a matrix, we will want to use a
purposeful data type implementing matrices, which (fingers crossed) hopefully
implements everything correctly for us so that we can abstract away from the
specific implementation details, such as whether the data is stored as lists
of lists, lists of tuples, dicts, or something else, and which guarantees for
us that when we expect a matrix we always have a valid matrix, with appropriate
error reporting when we try to do something that isn't compatible with
matrices.

Why you might want to use |project|
-----------------------------------

Because of all the issues with ad-hoc representations of matrix data discussed
above, there are plenty of packages implementing a matrix type
available on PyPI, and sometimes also custom implementations that just come
along as part of some other package which needed a matrix type. More often
than not, these implementations are incomplete, idiosyncratic and
unmaintained.

On the other hand, libraries such as NumPy and Pandas offer
extremely mature, well-maintained and performant implementations of matrix
types. They are a fantastic choice if you need to do hardcore, performant
number crunching or data analysis, but because they are built for specific
purposes they also come with specific requirements which might not fit your
needs -- they are to at least some degree domain-specific (at least in
their intentions and design), have an additional learning curve as they depart
in often significant and non-obvious ways from what one might expect based on
the standard built-in data types in Python (e.g. inclusive index slices in
Pandas, opposed to Pythons standard being always exclusive), and may impose
onerous requirements that might not be desirable, such as the need to install
a binary distribution or compile NumPy for the target system.

This is where the |project| package comes in, which offers two general-purpose
matrix data types: a mutable :class:`Matrix` type, and an immutable
:class:`FrozenMatrix` type.
Both are implemented in pure Python for maximal compatibility and
availability across systems and architectures, feature-rich, fully type
annotated (with the matrix types themselves being generic types), and closely
modelled after the existing standard built-in types in their functionality
and behaviour, which makes them more pythonic and intuitive to use, reduces
the learning curve, and avoids pitfalls due to unexpected idiosyncracies.
On the downside, they are definitely not as performant as for example NumPy
arrays, and they don't offer any facilities for multidimensional arrays --
they are just your regular boring old off-the-shelf two-dimensional matrices.
