import itertools
import logging
from typing import Callable, Dict, Set, Any, Tuple

logging.basicConfig(level=logging.INFO, format='%(message)s')
str_line = "-" * 30


class Arc:
    def __init__(self, arc):
        self.xi, self.xj = arc

    def __str__(self):
        return f"(x{self.xi}, x{self.xj})"

    def __repr__(self):
        return f"Arc(x{self.xi}, x{self.xj})"

    def __eq__(self, other):
        if not isinstance(other, Arc):
            return NotImplemented
        return self.xi == other.xi and self.xj == other.xj

    def __hash__(self):
        return hash((self.xi, self.xj))


class DomainWipeout(Exception):
    pass


# Types for Constraint Functions, Constraint Store and Domains
# xi, di, xj, dj parameter for ConstraintFunction Callables
ConstraintFunction = Callable[[int, Any, int, Any], bool]
ConstraintStore = Dict[Arc, ConstraintFunction]
InputDomains = Dict[int, Set]


class AC4:
    def ac4(self, input_domains: InputDomains, constraints: ConstraintStore):
        """Performs initial setup of data structures and runs the AC4 algorithm by calling the initialise and
        propagate methods.

        Args:
            input_domains (InputDomains): A dictionary of ints (decision variable ids) to the set of their
            possible values (domains)
            constraints (ConstraintStore): A dictionary of arcs to their Callable constraint function
        """

        logging.debug(str_line + "\nAC4: Beginning setup\n" + str_line)

        self.input_domains = input_domains
        self.constraints = constraints

        # Dictionary to store the number of supports for each domain element
        self.Counter = {(arc, di): 0 for arc in self.constraints.keys()
                        for di in self.input_domains[arc.xi]}

        # Dictionary that maps all domain elements to the elements it provides support
        self.S = {(xi, di): set() for xi in self.input_domains.keys()
                  for di in self.input_domains[xi]}

        # Table of deleted domain values - 1 if deleted otherwise 0
        self.M = {(xi, di): 0 for xi in self.input_domains.keys()
                  for di in self.input_domains[xi]}

        # List to contain value deletions to propagate
        self.L = list()

        logging.debug(
            "AC4: Initialized data structures for domains, constraints, Counter, S, M and L")

        logging.debug("AC4: Initial Domains = " +
                      ''.join([f'\nAC4: x{xi}: {Di} ' for xi, Di in self.input_domains.items()]))

        # A dictionary to contain the final domain outputs of AC4
        self.current_domains = {xi: set() for xi in self.input_domains.keys()}

        self.initialise()
        self.propagate()

    def initialise(self):
        """Processes all arcs once, enumerates support for each element of every domain and prunes
        domain elements with no supports. Stores any deletions in list L to propagate
        """
        logging.debug(str_line+"\nInitialise: Beginning Phase\n"+str_line)

        # For each Arc (xi, xj) and all pairs of their domain values di ∈ Di and dj ∈ Dj (skipping any deleted values)
        # If the pairs satisfy the constraint, increment the support counter for di and add it to the set S for
        # xj, dj to show the dj provides support for this assignment.

        try:
            for arc, constraint in self.constraints.items():
                for di in self.input_domains[arc.xi]:
                    for dj in self.input_domains[arc.xj]:
                        if self.M[(arc.xi, di)] != 1 or self.M[(arc.xj, dj)] != 1:
                            if self.checkConstraint(arc.xi, di, arc.xj, dj, constraint) == True:
                                self.S[arc.xj, dj].add((arc.xi, di))
                                self.Counter[(arc, di)] += 1

                                logging.debug(
                                    f"Initialise: Incremented counter {arc}, {di} = {self.Counter[(arc, di)]}")

                    # If no support for di and it hasn't already been removed, update M to show deletion and add deletion
                    # to L to propagate later.
                    if self.Counter[(arc, di)] == 0 and self.M[(arc.xi, di)] != 1:
                        self.M[(arc.xi, di)] = 1
                        self.L.append((arc.xi, di))
                        logging.debug(f"Initialise: deleting x{arc.xi}, {di}")

                        # Updates the current_domains dictionary when a value is deleted, by reading the switches in M
                        self.current_domains = {xi: set()
                                                for xi in self.input_domains.keys()}
                        for key, switch in self.M.items():
                            xi, di = key
                            if switch == 0:
                                self.current_domains[xi].add(di)
                        for xi, Di in self.current_domains.items():
                            if len(Di) == 0:
                                raise DomainWipeout
        except DomainWipeout:
            logging.info(
                f"Initialise: Domain wipeout detected, stopping AC4 algorithm")

        logging.debug(
            f"Initialise: List of deletions to propagate - {''.join([f'(x{xi}, {di}) ' for xi, di in self.L])}")

        logging.debug(
            "Initialise: Phase complete\n")

    def propagate(self):
        """Propagates deleted values in L by - iterating over the assignments supported by the deleted value (S)
         and decrementing their counters. If a counter reaches 0 and hasn't already been deleted then delete it
         and add to L. Continues until L is empty.
        """
        try:
            logging.debug(
                str_line + "\nPropagate: Beginning Phase\n" + str_line)
            while len(self.L) > 0:
                # Remove an element from L (arbitrarily decided to pick the first element but order is unimportant)
                xj, dj = self.L[0]
                self.L.pop(0)

                # Decrements the counters of assignments support by the deleted value
                for xi, di in self.S[(xj, dj)]:
                    arc = Arc((xi, xj))
                    self.Counter[(arc, di)] -= 1
                    logging.debug(
                        f"Propagate: updated counter {arc}, {di} = {self.Counter[(arc, di)]}")

                    # If a value has no supports and isn't already deleted, delete it and add to L
                    if self.Counter[(arc, di)] == 0 and self.M[(xi, di)] != 1:
                        self.M[(xi, di)] = 1
                        self.L.append((xi, di))
                        logging.debug(
                            f"Propagate: No supports found - deleting value x{xi}, {di}")

                        self.current_domains = {xi: set()
                                                for xi in self.input_domains.keys()}

                        for key, switch in self.M.items():
                            xi, di = key
                            if switch == 0:
                                self.current_domains[xi].add(di)

                        for xi, Di in self.current_domains.items():
                            if len(Di) == 0:
                                raise DomainWipeout
        except DomainWipeout:
            logging.info(
                f"Propagate: Domain wipeout detected, stopping AC4 algorithm")

        # Prints final domains
        logging.info(f"Propagate: Final Domains")
        for key, value in self.current_domains.items():
            logging.info(f"Propagate: x{key}: {value}")

        logging.debug(
            "Propagate: Phase complete")

    @ staticmethod
    def checkConstraint(xi, di, xj, dj, constraint) -> bool:
        """Calls the function from the constraint store on the 2 domain assignments for xi and dj.

        Args:
            xi (int): decision variable id 1
            di (Any): domain assignment 1
            xj (int): decision variable id 2
            dj (Any): domain assignment 2
            constraint (Callable): constraint function

        Returns:
            bool: if the constraint is satisfied or not
        """
        return constraint(xi, di, xj, dj)


# ----------------------------------------------------------------------------

# Constraint functions which are referenced in the ConstraintStore dictionary.
# Must take in parameters in the form (xi, di, xj, dj) -> bool

def nqueens_constraint(xi, di, xj, dj) -> bool:
    """nqueens constraint which ensures the two queens are not in the same row, column or diagonal.

    Args:
        xi (int): decision variable id 1
        di (Any): domain value 1
        xj (int): decision variable id 2
        dj (Any): domain value 2

    Returns:
        bool: if the assignments satisfy the constraint or not
    """
    if xi > xj:
        di, xi, dj, xj = dj, xj, di, xi

    return dj != di and dj != (di + xj - xi) and dj != (di - xj + xi)


def no_constraint(xi, di, xj, dj) -> bool:
    """Always returns true for an arc as there is no constraint between them

    Returns:
        bool: True
    """
    return True

# ----------------------------------------------------------------------------


def nqueens_ac4_test(num_queens, test_case):
    """Runs the AC4 algorithm on the nqueens problem by generating the required domains & constraints and calling 
    the AC4 class. Also restricts domains of decision variables defined by the test case to their single assigned
    value before running. 

    Args:
        num_queens: width of the chess board (i.e. number of queens to place)
        test_case: List of (xi, di) assignment pairs
    """
    # Creates domains/constraints - permutations used as no unary constraints applied
    domains = {n: set(range(num_queens)) for n in range(num_queens)}
    constraints = {Arc(n): nqueens_constraint for n in itertools.permutations(
        range(num_queens), 2)}

    # Restricts decision variables from the test case to be only the assigned value
    for xi, di in test_case:
        domains[xi] = set([di])

    # Runs the algorithm
    nqueensAC4 = AC4()
    nqueensAC4.ac4(domains, constraints)


# Test cases from assessment rubric - pairs of (xi, di) assignments
test_cases = [[(0, 0), (1, 2)],
              [(0, 0), (1, 3)],
              [(0, 1), (1, 3), (2, 5)]]


# Runs the three test cases as defined in the assessment brief
for case in test_cases:
    nqueens_ac4_test(num_queens=6, test_case=case)
