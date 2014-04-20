import unittest
import pickle
import shutil
import os
from dsdb import DeadSimple, WriteError, Value


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
        db.set('prego', Value(['hello']))
        self.assertTrue(os.path.exists('tests/db/prego'))

    def test_correct_content(self):
        db = DeadSimple('tests/db')
        db.set('prego', Value(['hello']))
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(['hello'], obj.get('content'))

    def test_internal_data_handling(self):
        db = DeadSimple('tests/db')
        db.set('prego', Value(['hello']))
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(0, obj.get('version'))
            self.assertEqual(['hello'], obj.get('content'))

        value = db.get('prego')
        value.content = 'hi'
        db.set('prego', value)
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(1, obj.get('version'))
            self.assertEqual('hi', obj.get('content'))

    def test_internal_data_handling_multiple_dbs(self):
        db1 = DeadSimple('tests/db')
        db1.set('prego', Value(['hello']))
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(0, obj.get('version'))
            self.assertEqual(['hello'], obj.get('content'))

        db2 = DeadSimple('tests/db')
        value = db2.get('prego')
        value.content = 'hi'
        db2.set('prego', value)
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(1, obj.get('version'))
            self.assertEqual('hi', obj.get('content'))

        db1 = DeadSimple('tests/db')
        value = db1.get('prego')
        value.content = ['howdy']
        db1.set('prego', value)
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(2, obj.get('version'))
            self.assertEqual(['howdy'], obj.get('content'))

    def test_set_must_fail_if_a_version_behind(self):
        db = DeadSimple('tests/db')
        db.set('prego', Value('hi'))
        self.assertRaises(WriteError, db.set, 'prego', Value('howdy'))

    def test_slash_not_allowed_in_key(self):
        db = DeadSimple('tests/db')
        self.assertRaises(KeyError, db.set, 'prego/ok', Value('hello'))

    def test_unsafe_set_must_always_update(self):
        db = DeadSimple('tests/db')
        db.unsafe_set('prego', Value('hi'))
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(0, obj.get('version'))
            self.assertEqual('hi', obj.get('content'))
        db.unsafe_set('prego', Value('hello'))
        with open('tests/db/prego', 'rb') as f:
            obj = pickle.loads(f.read())
            self.assertEqual(1, obj.get('version'))
            self.assertEqual('hello', obj.get('content'))

    def _appendable(self, value, stored):
        return Value(stored.content.union(value.content))

    def test_merge_method_implemented_as_callback(self):
        db = DeadSimple('tests/db')
        db.set('appendable', Value(set([1,2,3])), self._appendable)
        self.assertEqual(set([1,2,3]), db.get('appendable').content)
        db.set('appendable', Value(set([5,7])), self._appendable)
        self.assertEqual(set([1,2,3,5,7]), db.get('appendable').content)
