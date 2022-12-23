"""
This file declares optimized ways to resolve some algebra problems.

Here laying standard thinks. Some specified code that resolves specified
algebraic problems, can be written directly in the puzzle. So, all in the
file that can be used to build new functions included in __all__.

"""


from typing import Optional, Tuple
from operator import add


from .aliases import CoordinatesAlias, ScalarAlias


LineFunctionAlias = Tuple[ScalarAlias, ScalarAlias]  # y = kx + b  ->  (k, b)


def coordinates_sum(first: CoordinatesAlias, second: CoordinatesAlias):
    return tuple(map(lambda x: add(*x), zip(first, second)))


def line_segments_union(first: CoordinatesAlias, second: CoordinatesAlias) -> Optional[CoordinatesAlias]:
    """
    >>> line_segments_union((0, 2), (1, 3))
    (0, 3)
    >>> line_segments_union((1, 3), (0, 2))
    (0, 3)
    >>> line_segments_union((1, 1), (1, 1))
    (1, 1)

    Note that input where coord[0] > coord[1] is invalid

    """

    if first[0] > second[0]:
        first, second = second, first

    if first[1] >= second[0]:
        return first[0], second[1]
    else:
        return None


def line_segments_common(first: CoordinatesAlias, second: CoordinatesAlias) -> Optional[CoordinatesAlias]:
    """
    >>> line_segments_common((1, 3), (2, 3))
    (2, 3)
    >>> line_segments_common((1, 3), (3, 6))
    (3, 3)
    >>> line_segments_common((1, 3), (5, 6))
    None

    """

    if first[0] > second[0]:
        first, second = second, first

    if first[1] >= second[0]:
        return second[0], first[1]
    else:
        return None


def coordinates_to_line_function(first: CoordinatesAlias, second: CoordinatesAlias) -> LineFunctionAlias:
    """Resolve coordinates to the function y = kx + b

    :raises: ZeroDivisionError, if provided equation is x=x.

    """

    k = (second[1] - first[1]) / (second[0] - first[0])  # k = (y2-y1) / (x2-x1)

    b = first[1] - k * first[0]  # b = y - kx
    return k, b
