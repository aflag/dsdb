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
        db['prego'] = ['hello']
        self.assertRaises(KeyError, db.__getitem__, 'prego')
