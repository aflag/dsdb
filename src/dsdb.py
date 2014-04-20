import os
import time
import pickle
import fcntl
import collections
from contextlib import contextmanager


@contextmanager
def lock_file(*args, **kwargs):
    with open(*args, **kwargs) as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        # We need to open the file again in case it was modified while we were
        # waiting for the lock
        with open(*args, **kwargs) as f:
            yield f


class DeadSimple(object):
    """The dead simple database has a dead simple design:

    It is a key->value storage. Each key is a new file on the file system. The
    value can be any pickable object."""

    def __init__(self, directory):
        """Creates a database object.

        Keyword arguments:
        directory -- directory to save files into"""
        self.directory = directory

    def _read_from_file(self, f):
        data = f.read()
        if data:
            obj = pickle.loads(data)
        else:
            obj = {}
        return obj

    def __setitem__(self, key, value):
        """Synchronously values to disk under the specified key. It will always
        change the contents of disk, regardless of whether this object was the
        last one to modify the key or not."""
        if '/' in key:
            raise KeyError('Key cannot contain /: ' + key)
        file_name = os.path.join(self.directory, key)
        with lock_file(file_name, 'a+b') as f:
            f.seek(0)
            obj = self._read_from_file(f)
            obj['version'] = obj.get('version', -1) + 1
            obj['content'] = value
            obj['timestamp'] = int(round(time.time()))
            f.seek(0)
            f.truncate()
            f.write(pickle.dumps(obj))

    def __getitem__(self, key):
        """Retrieves whatever value is stored in disk. This method will block
        while a write is taking place."""
        if '/' in key:
            raise KeyError('Key cannot contain /: ' + key)
        file_name = os.path.join(self.directory, key)
        try:
            with lock_file(file_name, 'r') as f:
                obj = self._read_from_file(f)
                return obj['content']
        except IOError, e:
            if e.errno == 2:
                raise KeyError('Key "' + key + '" not found')
            else:
                raise e
