import itertools
from typing import Any, Callable, DefaultDict

# Type hints for the Arcs, Constraint Functions and Constraint Store
Arc = (int, int)
ConstraintFunction = Callable[[(int, int), (int, int)], bool]
ConstraintStore = Dict[Arc, ConstraintFunction]


class AC4:
    def __init__(self, d):
        # TODO: Define the integer decision variables

        # TODO: Define binary constraint data structure
        pass


def nqueens_constraint(q1, q2):
    i, xi = q1
    j, xj = q2
    return (xj != xi) and (xj != xi + j - i) and (xj != xi - j - i)
