Matrix types for Python
=======================

The *matrix-types* package implements simple and intuitive matrix data types for
Python.

Matrixes are often required to implement various algorithms or store
and process two-dimensional data arrays. While this can be (and often is)
achieved with built-in data types, such as lists of lists or tuples of tuples,
these approaches frequently require a programmatic approach that is aware of
the internal structure of the data, and because of the arbitrary lengths of
types such as :code:`list` and :`tuple` they offer little in the way
of assurances that their internal structure is (and remains) consistent.

The :code:`Matrix` and :code:`FrozenMatrix` types in the *matrix-types*
package implement mutable and immutable matrix data types with an interface
modelled closely on Python's built-in data types, such as :code:`list`,
:code:`tuple`, and :code:`dict` -- if you know how to use these you
probably already know how to use :code:`Matrix` and
:code:`FrozenMatrix`! The matrix types implemented here are also fully type
annotated and support generic types, meaning you can use static type checkers
such as `mypy <https://www.mypy-lang.org/>`_ to avoid or spot potential issues
in your code before they become a problem.


Installation
============

Installing *matrix-types* is easiest via :code:`pip install` from
`PyPI <https://pypi.org>`, which will get you the latest release.

Installation on Linux and most other \*nix-es:

.. code-block:: bash

   $ python3 -m pip install matrix-types

Installation on Windows:

.. code-block:: powershell

   py -m pip install matrix-types


Getting started
===============

The actual Python package installed by *matrix-types* is called
:code:`matrices`, and this will be available to import as such after
installation. Simply import this package and you're ready to start exploring
the :code:`Matrix` and :code:`FrozenMatrix` types.

Example::

   from matrices import Matrix

   m = Matrix([1, 2, 3, 4, 5, 6], shape=(2, 3), default=0)
   print("Hello matrix:\n", m)

Output::

   Hello matrix:
        0  1  2
      ┌         ┐
    0 │ 1  2  3 │
    1 │ 4  5  6 │
      └         ┘


**For the full documentation see https://matrices.readthedocs.io/.**
