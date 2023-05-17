import operator
from functools import partial
from itertools import islice, starmap, product
from typing import Iterable, Iterator, Sequence, TypeVar

_T = TypeVar("_T")


def chunked(iterable: Iterable[_T], n: int) -> Iterator[list[_T]]:
    """Break *iterable* into lists of length *n*."""
    return iter(partial(lambda _ib: list(islice(_ib, n)), iter(iterable)), [])


def _anysum(iterable: Iterable[_T]) -> _T:
    """Compute repeated addition of values in a non-empty iterable."""
    it = iter(iterable)
    try:
        result = next(it)
    except StopIteration:
        raise ValueError("iterable must not be empty")
    for value in it:
        try:
            result = result + value  # type: ignore
        except TypeError:
            raise TypeError(
                "incompatible operand type(s) for +: "
                f"{type(result)!r} and {type(value)!r}"
            )
    return result


def _sumprod(vec1: Iterable[_T], vec2: Iterable[_T]) -> _T:
    """Compute a sum of producs."""
    return _anysum(starmap(operator.mul, zip(vec1, vec2, strict=True)))  # type: ignore


def matmul(m1: Iterable[Iterable[_T]], m2: Sequence[Sequence[_T]]) -> Iterator[list[_T]]:
    """Multiply to matrices represented as iterables."""
    return chunked(starmap(_sumprod, product(m1, zip(*m2, strict=True))), len(m2[0]))
