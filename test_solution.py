"""Test to make sure that our solution works for the sql implementations"""
from .solution import create_analysis_table
from . import solution
from .. import models
from ..resources import db
import unittest


class TestSolution(unittest.TestCase):

    def setUp(self):
        print('set up')
        session = db.make_session()
        session.query(models.SQLSolutionRow).delete()
        session.commit()

    def tearDown(self):
        print('tear down')
        session = db.make_session()
        session.query(models.SQLSolutionRow).delete()
        session.commit()

    def test_get_summary(self):
        """test that it returns an empty dictionary if asked to summarize empty results list"""
        result = solution.get_summary([])
        self.assertEqual(result, {})

    def test_solution(empty_sql_solution_table):
        """ Test our solution worked! Right now just tests we wrote a dummy row."""
        create_analysis_table()
        session = db.make_session()
        rows = session.query(models.SQLSolutionRow).all()
        print(f'{len(rows)} rows added')
        assert len(rows) >= 1


if __name__ == '__main__':
    unittest.main()
