import unittest
import pickle
import shutil
import os
from dsdb import DeadSimple, Value


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
        db.set('prego', Value(['hello']))
        self.assertRaises(KeyError, db.get, 'prego/ok')

    def test_key_not_found(self):
        db = DeadSimple('tests/db')
        self.assertRaises(KeyError, db.get, 'prego')

    def test_read_written_data(self):
        db = DeadSimple('tests/db')
        db.set('prego', Value(['hello']))
        self.assertEqual(['hello'], db.get('prego').content)

    def test_multiple_dbs(self):
        db1 = DeadSimple('tests/db')
        db1.set('prego', Value(['hello']))
        self.assertEqual(['hello'], db1.get('prego').content)

        db2 = DeadSimple('tests/db')
        value = db2.get('prego')
        value.content = ['howdy']
        db2.set('prego', value)
        self.assertEqual(['howdy'], db2.get('prego').content)

        db1 = DeadSimple('tests/db')
        value = db1.get('prego')
        value.content = ['hi']
        db1.set('prego', value)
        self.assertEqual(['hi'], db1.get('prego').content)
