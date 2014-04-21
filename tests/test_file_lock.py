import unittest
import threading
import time
import os
from dsdb import lock_file


class FileLockingThread(threading.Thread):

    def run(self):
        self.execution_point = 'before lock'
        with lock_file('tests/file', 'wb') as f:
            self.execution_point = 'after lock'
            f.write('inside thread')
        self.execution_point = 'method ending'


class TestFileLock(unittest.TestCase):

    def tearDown(self):
        try:
            os.unlink('tests/file')
        except:
            pass

    def test_write_to_file(self):
        with lock_file('tests/file', 'wb') as f:
            f.write('things')
        with open('tests/file', 'rb') as f:
            self.assertEqual('things', f.read())

    def test_write_twice_to_file(self):
        with lock_file('tests/file', 'wb') as f:
            f.write('things')
        with lock_file('tests/file', 'wb') as f:
            f.write('my things')
        with open('tests/file', 'rb') as f:
            self.assertEqual('my things', f.read())

    def test_write_twice_big_first_to_file(self):
        with lock_file('tests/file', 'wb') as f:
            f.write('my things')
        with lock_file('tests/file', 'wb') as f:
            f.write('things')
        with open('tests/file', 'rb') as f:
            self.assertEqual('things', f.read())

    def test_file_locking(self):
        t = FileLockingThread()
        with lock_file('tests/file', 'wb') as f:
            t.start()
            time.sleep(0.2)
            self.assertEqual('before lock', t.execution_point)
            f.write('outside thread')
        time.sleep(0.2)
        with open('tests/file', 'rb') as f:
            self.assertEqual('inside thread', f.read())
