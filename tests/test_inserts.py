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
            self.assertEqual(['hello'], obj)

    def test_slash_not_allowed_in_key(self):
        db = DeadSimple('tests/db')
        db['prego'] = ['hello']
        self.assertRaises(ValueError, db.__setitem__, 'prego/ok', 'hello')
