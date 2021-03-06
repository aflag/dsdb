Dead Simple Database
====================

Simple. Simple use, for simple needs.

Goals
=====

* It should be slow (IOW, speed is *not* a concern)
* It must be schemaless
* It must be easy to use
* It must be easy to code
* It must not require anything, but a unix filesystem
* It must be safe to use with concurrent processes (and threads)

Install
=======

Use pip to do it:

```
pip install -e git://github.com/aflag/dsdb@0.1#egg=dsdb
```

Notice that you can add

```
-e git://github.com/aflag/dsdb@0.1#egg=dsdb
```

to your requirements.txt.

Example
=======

```python
from dsdb import DeadSimple, Value, WriteError

db = DeadSimple('/tmp/db/')
db.set('key1', Value('hey'))
value = db.get('key1')

print value.content  #=> hey

value.content = 'another thing'
db.set('key1', value)
value = db.get('key1')

print value.content  #=> another thing

try:
    db.set('key1', Value("ops, an error!"))
except WriteError:
    # value's version is older than what's in storage
    pass
db.set_unsafe('key1', Value("all is well"))  # this should work regardless of version

print db.get('key1').content  #=> all is well
```

Architecture
============

Each key is stored in a different file inside a db directory. I use
flock to guarantee data consistency. That means only one process can
read or update a file at a time.

A backup can be done merely copying all files inside the directory
(extra points for those of you who use flock on your backup script :)

That's it.

Improvements
============

Although speed is not a primary concern, there are easy things that can
be developed later to improve on it. One is to keep a memory cache for
reads.  Using inotify, I could invalidate the in-memory cache whenever a
key gets written to. That would work as long as the number of reads is
much greater than the number of writes.

Benchmark
=========

On quick 'n' dirty benchmark using timeit (look at tests/benchmark.py) I
got 640 read+writes per second. That is, I made 640 reads and 640 writes
in one second. That's about the worst case scenario (the read
improvement outlined may very well make that number a lot bigger). I ran
that benchmark on my lenovo desktop, which has SSD HD. Please run it
yourself and report back :)

My desktop PC (with old disk based HD) set me back to 436 reads+writes
per second. My linode machine, which supposely uses SSD, gets me 379
reads+writes per second.

It all comes to show that reading and writing to disk is not THAT slow
:P Thankfully all those numbers are bigger than what I need :)
