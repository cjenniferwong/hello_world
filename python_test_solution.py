from . import solution
from .. import models
from ..resources import db
import unittest


class TestSolution(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('set up class')
        pass

    def tearDownClass(cls):
        print('tear down class')
        pass

    def setUp(self):
        print('set up')
        pass

    def tearDown(self):
        print('tear down')
        pass

    def test_solution(empty_python_solution_table):
        """ Test our solution worked! Right now just tests we wrote a dummy row."""
        print('test solution')

        solution.create_analysis_table()
        rows = solution.read_all_rows(models.PythonSolutionRow)

        assert len(rows) == 1

        row = rows[0]

        assert row.primary_diag_code == "1234.56"
        assert row.age_bracket == "0-4"
        assert row.num_unique_patients == 123


if __name__ == '__main__':
    unittest.main()
