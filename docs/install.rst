Installation and requirements
=============================


Requirements
------------

|project| should run on any machine that runs `Python <https://python.org>`_
version 3.10 or newer.

There are no other requirements, and only a single dependency
(`more-itertools <https://pypi.org/project/more-itertools/>`_),
which will be installed automatically if you use :command:`pip` as shown
below.


Installation
------------

Installing |project| is easiest via :command:`pip install` from
`PyPI <https://pypi.org>`_, which will get you the latest release.

.. code-block:: bash
   :caption: Installation on Linux and most other \*nix-es

   $ python3 -m pip install matrix-types

.. code-block:: powershell
   :caption: Installation on Windows

   py -m pip install matrix-types


To install the very latest, potentially unstable, in-development version
directly from the github (*not recommended* --- this should normally only be used
for testing), you can also run
:code:`python3 -m pip install "matrices @ git+https://github.com/thatfloflo/matrix-types.git@main"`.


Getting started
---------------

The actual Python package installed by |project| is called :code:`matrices`,
and this will be available to import as such after installation. Simply
import this package and you're ready to start exploring the :class:`Matrix` and
:class:`FrozenMatrix` types.

You can either import the entire :code:`matrices` package, for example::

   import matrices

   m = matrices.Matrix([1, 2, 3, 4, 5, 6], shape=(2, 3), default=0)
   print("Hello matrix:\n", m)

::

   Hello matrix:
        0  1  2
      ┌         ┐
    0 │ 1  2  3 │
    1 │ 4  5  6 │
      └         ┘

Or you can import just the components you need, for example::

    from matrices import Matrix, FrozenMatrix

    m = Matrix([1, 2, 3, 4, 5, 6], shape=(2, 3), default=0)
    n = FrozenMatrix(range(1, 7), (2, 3), default=0)

    if m == n:
        print(f"Both matrices have the same shape and values, namely:\n{m}")
    else:
        print("The matrices are different..")
        print(f"m is ..\n{m}")
        print(f"n is ..\n{n}")

::

   Both matrices have the same shape and values, namely:
        0  1  2
      ┌         ┐
    0 │ 1  2  3 │
    1 │ 4  5  6 │
      └         ┘

The next section, :doc:`usage`, will give a more detailed overview of all the
various things that can be done with the matrix types included in |project|.
