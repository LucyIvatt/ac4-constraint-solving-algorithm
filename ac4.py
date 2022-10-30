import itertools
import logging
from typing import Any, Callable, Dict, Set, Tuple

logging.basicConfig(level=logging.DEBUG)


class DecisionVar:
    def __init__(self, id, val):
        self.id = id
        self.value = value


class Arc:
    def __init__(self, arc):
        self.i, self.j = arc

    def __str__(self):
        return f"(x{self.i}, x{self.j})"

    def __repr__(self):
        return f"Arc(x{self.i}, x{self.j})"


# Type hints for the Arcs, Constraint Functions and Constraint Store
ConstraintFunction = Callable[[DecisionVar, DecisionVar], bool]
ConstraintStore = Dict[Arc, ConstraintFunction]
Domains = Dict[int, Set]


class AC4:
    def __init__(self, domains: DecisionVar, constraints: ConstraintStore):
        self.domains = domains
        self.constraints = constraints

        self.Counter = {(arc, val): 0 for arc in self.constraints.keys()
                        for val in domains[arc.i]}

        self.S = {(var, val): set() for var in self.domains.keys()
                  for val in self.domains[var]}

        self.M = {(var, val): 0 for var in self.domains.keys()
                  for val in self.domains[var]}

        self.L = list()

        self.initialise()
        self.propagate()

    def set_decision_var(self, var, value):
        self.domains[var] = set(value)

    def initialise(self):
        logging.debug("Initialise: Beginning initialization")
        for arc, constraint in self.constraints.items():
            for di in self.domains[arc.i]:
                for dj in self.domains[arc.j]:
                    if self.M[(arc.i, di)] != 1 or self.M[(arc.j, dj)] != 1:
                        if self.checkConstraint(arc.i, di, arc.j, dj, constraint) == True:
                            self.S[arc.j, dj].add((arc.i, di))
                            self.Counter[(arc, di)] += 1
                            logging.debug(
                                f"Initialise: set counter {arc}, {di} = {self.Counter[(arc, di)]}")

                if self.Counter[(arc, di)] == 0 and self.M[(arc.i, di)] != 1:
                    self.M[(arc.i, di)] = 1
                    self.L.append((arc.i, di))
                    logging.debug(f"Initialise: deleting x{arc.i}, {di}")

                for key in self.Counter:
                    print(type(key))

        logging.debug(
            f"Initialise: List of deletions to propagate - {''.join([f'(x{d[0]}, {d[1]}) ' for d in self.L])}")

    def propagate(self):
        for key in self.Counter:
            print(key, " ", type(key))
        print(type((Arc((1, 0)), 21)))
        self.Counter[(Arc((1, 0)), 21)]
        # # while L is not empty
        # while len(self.L) > 0:
        #     # Remove an element from L
        #     xj, dj = self.L[0]
        #     self.L.pop(0)

        #     for xi, di in self.S[(xj, dj)]:
        #         arc = Arc((xi, xj))
        #         self.Counter[(arc, di)] -= 1
        #         logging.debug(
        #             f"Propagate: updated counter {arc}, {xi} = {self.Counter[(arc, xi)]}")
        #         if self.Counter[(arc, di)] == 0 and self.M[(xi, di)] != 1:
        #             self.M[(xi, di)] = 1
        #             self.L.append((xi, di))
        #             logging.debug(
        #                 f"Propagate: deleting value x{xi}, {di}")

        # # Prints out final domains
        # print(M)

    @ staticmethod
    def checkConstraint(i, xi, j, xj, constraint):
        return constraint(i, xi, j, xj)


def nqueens(i, xi, j, xj):
    return (xj != xi) and (xj != xi + j - i) and (xj != xi - j - i)


def less_than(i, xi, j, xj):
    return xi < xj


def greater_than(i, xi, j, xj):
    return xi > xj


# Testing with NQueens Problem
# domains = {n: set(range(6)) for n in range(6)}
# constraints = {Arc(n): nqueens for n in itertools.combinations(range(6), 2)}
# ac4 = AC4(domains, constraints)

# Testing with Lecture Example
domains = {0: {2, 10, 16}, 1: {9, 12, 21},
           2: {9, 10, 11}, 3: {2, 5, 10, 11}}
constraints = {Arc((0, 1)): less_than,
               Arc((0, 2)): less_than,
               Arc((0, 3)): less_than,
               Arc((1, 0)): greater_than,
               Arc((1, 2)): less_than,
               Arc((1, 3)): less_than,
               Arc((2, 0)): greater_than,
               Arc((2, 1)): greater_than,
               Arc((2, 3)): greater_than,
               Arc((3, 0)): greater_than,
               Arc((3, 1)): greater_than,
               Arc((3, 2)): less_than}
ac4graph = AC4(domains, constraints)
