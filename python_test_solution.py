"""Test to make sure that our solution works for the python implementations"""

from . import solution
from .. import models
from ..resources import db
from ..constants import INVALID_BIRTH_DATE, INVALID_CLAIM_DATE
import unittest


class TestSolution(unittest.TestCase):

    def setUp(self):
        session = db.make_session()
        session.query(models.PythonSolutionRow).delete()
        session.commit()

    def tearDown(self):
        session = db.make_session()
        session.query(models.PythonSolutionRow).delete()
        session.commit()

    def test_bad_birth_date(self):
        """ Test what happens if we have a bad birth date entry"""
        self.service = solution.Services(
            1, '23', '2009-09-09', '0', '')
        self.assertEqual(self.service.patient_birth_date, INVALID_BIRTH_DATE)

    def test_bad_claim_date(self):
        """ Test what happens if we have a bad claim date entry"""
        self.service = solution.Services(
            1, '23', '', '0', '2020/Jan/01')
        self.assertEqual(self.service.claim_date, INVALID_CLAIM_DATE)

    def test_get_summary(self):
        """
        test if we query the database and get no results
        """
        test_empty_query_results = []
        result = solution.get_summary(test_empty_query_results)
        self.assertEqual(result, {})

    def test_write_summary_rows(self):
        """
        test if we query the database and get no results, do we write no rows?
        """
        test_summary_rows = []
        solution.write_summary_rows(test_summary_rows)
        rows = solution.read_all_rows(models.PythonSolutionRow)
        self.assertEqual(len(rows), 0)

    def test_solution(empty_python_solution_table):
        """ Test our solution worked! Right now just tests we wrote a dummy row."""

        solution.create_analysis_table()
        rows = solution.read_all_rows(models.PythonSolutionRow)
        print(f'{len(rows)} rows added')
        assert len(rows) >= 10000


if __name__ == '__main__':
    unittest.main()
