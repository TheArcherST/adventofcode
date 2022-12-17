from _2022.day_15 import functions_overlay, FunctionOverlayStatus, fractions_overlay

from utils.algebra import coordinates_to_line_function


def test_functions_overlay():
    f1 = coordinates_to_line_function((2, 1), (5, 4))
    f2 = coordinates_to_line_function((2, 5), (5, 2))
    f3 = coordinates_to_line_function((6, 5), (7, 6))
    f4 = coordinates_to_line_function((8, 5), (6, 3))

    assert functions_overlay(f1, f1) == (FunctionOverlayStatus.PARALLEL, None)
    assert functions_overlay(f1, f2) == (FunctionOverlayStatus.SINGLE_INTERSECTION, (4, 3))
    assert functions_overlay(f1, f3) == (FunctionOverlayStatus.PARALLEL, None)
    assert functions_overlay(f1, f4) == (FunctionOverlayStatus.NO_INTERSECTION, None)

    assert functions_overlay(f2, f1) == (FunctionOverlayStatus.SINGLE_INTERSECTION, (4, 3))
    assert functions_overlay(f2, f2) == (FunctionOverlayStatus.PARALLEL, None)
    assert functions_overlay(f2, f3) == (FunctionOverlayStatus.SINGLE_INTERSECTION, (4, 3))
    assert functions_overlay(f2, f4) == (FunctionOverlayStatus.SINGLE_INTERSECTION, (5, 2))

    assert functions_overlay(f3, f1) == (FunctionOverlayStatus.PARALLEL, None)
    assert functions_overlay(f3, f2) == (FunctionOverlayStatus.SINGLE_INTERSECTION, (4, 3))
    assert functions_overlay(f3, f3) == (FunctionOverlayStatus.PARALLEL, None)
    assert functions_overlay(f3, f4) == (FunctionOverlayStatus.NO_INTERSECTION, None)

    assert functions_overlay(f4, f1) == (FunctionOverlayStatus.NO_INTERSECTION, None)
    assert functions_overlay(f4, f2) == (FunctionOverlayStatus.SINGLE_INTERSECTION, (5, 2))
    assert functions_overlay(f4, f3) == (FunctionOverlayStatus.NO_INTERSECTION, None)
    assert functions_overlay(f4, f4) == (FunctionOverlayStatus.PARALLEL, None)


def test_fractions_overlay():
    fraction_1 = ((1, 0), (4, 3), (1,))
    fraction_2 = ((3, 2), (6, 5), (2,))

    assert fractions_overlay(fraction_1, fraction_2) == ((((1, 0), (3, 2), (1,)),
                                                         ((3, 2), (4, 3), (1, 2)),
                                                         ((4, 3), (6, 5), (2,))), None)

    fraction_1 = ((5, 2), (2, 5), (1,))
    fraction_2 = ((3, 2), (5, 4), (2,))

    assert fractions_overlay(fraction_1, fraction_2) == ((fraction_1, fraction_2), (4, 3))

    fraction_1 = ((15, 15), (10, 10), (1,))
    fraction_2 = ((3, 2), (5, 4), (2,))

    assert fractions_overlay(fraction_1, fraction_2) == ((fraction_1, fraction_2), None)
