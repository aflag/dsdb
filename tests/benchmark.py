import sys
import os
import random
import shutil
sys.path.append('src')
from dsdb import DeadSimple, Value

def dsdb_worst_case():
    db = DeadSimple('tests/db')
    keys = 'agua mole em pedra dura tanto bate ate que fura'.split()
    random.shuffle(keys)
    for key in keys:
        try:
            value = db.get(key)
        except KeyError:
            value = Value(key)
        value.content = keys[0]
        db.set(key, value)
        

if __name__ == '__main__':
    import timeit
    os.mkdir('tests/db')
    try:
        N = 5000
        print float(N)/timeit.timeit("dsdb_worst_case()", setup="from __main__ import dsdb_worst_case", number=N), 'cases per seconds'
    finally:
        shutil.rmtree('tests/db')
