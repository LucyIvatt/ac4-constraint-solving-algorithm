import unittest

from ac4 import nqueens_constraint


class TestNQueensCons(unittest.TestCase):
    def test_constraint_col_up(self):
        xi, di, xj, dj = 3, 3, 1, 3
        self.assertFalse(nqueens_constraint(xi, di, xj, dj))

    def test_constraint_col_down(self):
        xi, di, xj, dj = 2, 1, 5, 1
        self.assertFalse(nqueens_constraint(xi, di, xj, dj))

    def test_constraint_diag_left(self):
        xi, di, xj, dj = 1, 3, 3, 1
        self.assertFalse(nqueens_constraint(xi, di, xj, dj))

    def test_constraint_diag_right(self):
        xi, di, xj, dj = 2, 3, 4, 5
        self.assertFalse(nqueens_constraint(xi, di, xj, dj))


if __name__ == '__main__':
    unittest.main()
