import unittest
import pickle
import shutil
import os
from dsdb import DeadSimple


class TestInserts(unittest.TestCase):

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

    def test_file_created(self):
        db = DeadSimple('tests/db')
        db['prego'] = ['hello']
        self.assertTrue(os.path.exists('tests/db/prego'))

    def test_correct_content(self):
        db = DeadSimple('tests/db')
        db['prego'] = ['hello']
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(['hello'], obj.get('content'))

    def test_internal_data_handling(self):
        db = DeadSimple('tests/db')
        db['prego'] = ['hello']
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(0, obj.get('version'))
            self.assertEqual(['hello'], obj.get('content'))

        db['prego'] = 'hi'
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(1, obj.get('version'))
            self.assertEqual('hi', obj.get('content'))

    def test_internal_data_handling_multiple_dbs(self):
        db1 = DeadSimple('tests/db')
        db1['prego'] = ['hello']
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(0, obj.get('version'))
            self.assertEqual(['hello'], obj.get('content'))

        db2 = DeadSimple('tests/db')
        db2['prego'] = 'hi'
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(1, obj.get('version'))
            self.assertEqual('hi', obj.get('content'))

        db1 = DeadSimple('tests/db')
        db1['prego'] = ['howdy']
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(2, obj.get('version'))
            self.assertEqual(['howdy'], obj.get('content'))

    def test_slash_not_allowed_in_key(self):
        db = DeadSimple('tests/db')
        db['prego'] = ['hello']
        self.assertRaises(KeyError, db.__setitem__, 'prego/ok', 'hello')
