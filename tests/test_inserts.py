import unittest
import shutil
import os
from dsdb import DeadSimple


class TestInsertFunction(unittest.TestCase):

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

    def test_version_increment(self):
        db = DeadSimple('tests/db')
        db['prego'] = ['hello']
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(0, obj.get('version'))

        db['prego'] = 'hi'
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(1, obj.get('version'))

    def test_version_increment_with_multiple_dbs(self):
        db1 = DeadSimple('tests/db')
        db1['prego'] = ['hello']
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(0, obj.get('version'))

        db2 = DeadSimple('tests/db')
        db2['prego'] = 'hi'
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(1, obj.get('version'))

        db1 = DeadSimple('tests/db')
        db1['prego'] = ['hello']
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(3, obj.get('version'))

    def test_slash_not_allowed_in_key(self):
        db = DeadSimple('tests/db')
        db['prego'] = ['hello']
        self.assertRaises(ValueError, db.__setitem__, 'prego/ok', 'hello')
