import os
import time
import pickle
import fcntl
import collections
from contextlib import contextmanager


class WriteError(Exception):
    pass


@contextmanager
def lock_file(*args, **kwargs):
    with open(*args, **kwargs) as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        # We need to open the file again in case it was modified while we were
        # waiting for the lock
        with open(*args, **kwargs) as f:
            yield f


class Value(object):
    """I wish this DTO class did not exist. But I rather have it explicit, than
    to create an obscure attribute on user's object. The purpose of this class
    is to hold a version variable, used to know if the value we are going to
    add is newer than the value that's written on the database."""

    def __init__(self, content):
        """Keywords arguments:
        content -- whatever data you need to store, as long as it's pickable"""
        self.content = content
        self.version = -1

    def __eq__(self, other):
        return self.version==other.version and self.content==other.content


class DeadSimple(object):
    """The dead simple database has a dead simple design:

    It is a key->value storage. Each key is a new file on the file system. The
    value can be any pickable object.

    Why do you use get and set methods instead of __getitem__ and __setitem__?

    Because I feel like db['key'].content = 'new value' looks like it would
    change the contents in disk. While that's not actually true."""

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

    def unsafe_set(self, key, value):
        """Does the same as set, but ignores whatever is stored and always add
        the new value."""
        self.set(key, value, merge=lambda value,stored: value)

    def change(self, key, change_cb):
        """Calls change_cb(stored_value)->new_value inside the critical section
        of the file update. None is passed as the value content if the key is
        empty. The returned value of change_cb will be added to storage."""
        value = Value(None)
        value.version = -2  # guarantees version is always old
        self.set(key, value, lambda value, stored_value: change_cb(stored_value))

    def set(self, key, value, merge=None):
        """Synchronously values to disk under the specified key. It will always
        change the contents of disk, regardless of whether this object was the
        last one to modify the key or not.

        Keyword arguments:
        key -- tag to file the value under
        value -- An Value object contained the user pickable object
        merge -- If merge(value, stored_value)->new_value is set, then instead
        of raising a WriteError, we use it to merge the stored value with the
        new value. This is done to make the user's life easier when there's a
        version conflict."""
        if '/' in key:
            raise KeyError('Key cannot contain /: ' + key)
        file_name = os.path.join(self.directory, key)
        with lock_file(file_name, 'a+b') as f:
            obj = self._read_from_file(f)
            if value.version >= obj.get('version', -1):
                obj['content'] = value.content
            elif merge is not None:
                stored_value = Value(obj.get('content'))
                stored_value.version = obj.get('version', -1)
                obj['content'] = merge(value, stored_value).content
            else:
                raise WriteError("Stored version is newer than ours")
            obj['version'] = obj.get('version', -1) + 1
            f.seek(0)
            f.truncate()
            f.write(pickle.dumps(obj))

    def get(self, key):
        """Retrieves whatever value is stored in disk. This method will block
        while a write is taking place.

        Keyword Arguments:
        key -- tag under which the value was stored

        Return:
        A value object containing user's value and a version."""
        if '/' in key:
            raise KeyError('Key cannot contain /: ' + key)
        file_name = os.path.join(self.directory, key)
        try:
            with lock_file(file_name, 'r') as f:
                obj = self._read_from_file(f)
                value = Value(obj['content'])
                value.version = obj['version']
                return value
        except IOError, e:
            if e.errno == 2:
                raise KeyError('Key "' + key + '" not found')
            else:
                raise e
