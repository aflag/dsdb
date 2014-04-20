import unittest
import pickle
import shutil
import os
from dsdb import DeadSimple


class TestReads(unittest.TestCase):

    def setUp(self):
        try:
            shutil.rmtree('tests/db')
        except:
            pass
        os.mkdir('tests/db')
        
    def tearDown(self):
        try:
            shutil.rmtree('tests/db')
        except:
            pass

    def test_slash_not_allowed_in_key(self):
        db = DeadSimple('tests/db')
        db['prego'] = ['hello']
        self.assertRaises(KeyError, db.__getitem__, 'prego/ok')

    def test_key_not_found(self):
        db = DeadSimple('tests/db')
        self.assertRaises(KeyError, db.__getitem__, 'prego')

    def test_read_written_data(self):
        db = DeadSimple('tests/db')
        db['prego'] = ['hello']
        self.assertEqual(['hello'], db['prego'])

    def test_multiple_dbs(self):
        db1 = DeadSimple('tests/db')
        db1['prego'] = ['hello']
        self.assertEqual(['hello'], db1['prego'])

        db2 = DeadSimple('tests/db')
        db2['prego'] = ['howdy']
        self.assertEqual(['howdy'], db2['prego'])

        db1 = DeadSimple('tests/db')
        db1['prego'] = ['hi']
        self.assertEqual(['hi'], db1['prego'])
