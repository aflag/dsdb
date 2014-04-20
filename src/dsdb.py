import os


class DeadSimple(object):
    """The dead simple database has a dead simple design:

    It is a key->value storage. Each key is a new file on the file system. The
    value can be any pickable object."""

    def __init__(self, directory):
        """Creates a database object.

        Keyword arguments:
        directory -- directory to save files into"""
        self.directory = directory
        self.keys = {}

    def __setitem__(self, key, value):
        pass
