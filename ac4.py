import itertools
from typing import Any, Callable, Dict, Set, Tuple


class DecisionVar:
    def __init__(self, id, val):
        self.id = id
        self.value = value


class Arc:
    def __init__(self, arc):
        self.i, self.j = arc

    def __str__(self):
        return f"({self.i}, {self.j})"

    def __repr__(self):
        return f"Arc({self.i}, {self.j})"


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

    def set_decision_var(self, var, value):
        self.domains[var] = set(value)

    def initialise(self):
        for arc, constraint in self.constraints.items():
            # print("Checking ", arc)
            for di in self.domains[arc.i]:
                for dj in self.domains[arc.j]:
                    if self.M[(arc.i, di)] != 1 or self.M[(arc.j, dj)] != 1:
                        print("checking ", di, " ", constraint, " ", dj)
                        if self.checkConstraint(arc.i, di, arc.j, dj, constraint) == True:
                            print("meets constraint")
                            self.S[arc.j, dj].add((arc.i, di))
                            self.Counter[(arc, di)] += 1
                    else:
                        pass
                        # print("one was deleted")
                if self.Counter[(arc, di)] == 0:
                    print("deleting ", arc.i, " ", di)
                    self.M[(arc.i, di)] = 1
                    self.L.append((arc.i, di))
            for key, value in self.Counter.items():
                print(key, value)
        print(self.M)

    @staticmethod
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
ac4graph.initialise()
