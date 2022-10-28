import itertools
from typing import Any, Callable, DefaultDict

Arc = (int, int)
ConstraintFunction = Callable[[Any, Any], bool]
ConstraintStore = Dict[Arc, ConstraintFunction]


class AC4:
    def __init__(self, d):
        # TODO: Define the integer decision variables

        # TODO: Define binary constraint data structure
        pass


def nqueens_constraint(q1, q2):
    return (q2 != q1) and (q2 != q1 + j - i) and (q2 != q1 - j - i)
