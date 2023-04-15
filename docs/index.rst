Matrix types for Python
=======================

The |project| package implements simple and intuitive matrix data types for
Python. Matrixes are often required to implement various algorithms or store
and process two-dimensional data arrays. While this can be (and often is)
achieved with built-in data types, such as lists of lists or tuples of tuples,
these approaches frequently require a programmatic approach that is aware of
the internal structure of the data, and because of the arbitrary lengths of
types such as :py:obj:`list` and :py:obj:`tuple` they offer little in the way
of assurances that their internal structure is (and remains) consistent.

The :class:`Matrix` and :class:`FrozenMatrix` types in the |project| package
implement mutable and immutable matrix data types with an interface modelled
closely on Python's built-in data types, such as :py:obj:`list`,
:py:obj:`tuple`, and :py:obj:`dict` -- if you know how to use these you
probably already know how to use :class:`Matrix` and :class:`FrozenMatrix`!
The matrix types implemented here are also fully type annotated and support
generic types, meaning you can use static type checkers such as *mypy* to
avoid or spot potential issues in your code before they become a problem.


.. toctree::
   :maxdepth: 2
   :caption: Contents

   preliminaries
   basics
   api



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
