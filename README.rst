rdl - Redis dump-load tool
==========================

.. image:: https://travis-ci.org/reorx/rdl.svg?branch=master
    :target: https://travis-ci.org/reorx/rdl

This tool is made specially for dump & load certain database of a redis server,
if you want to dump whole redis or replicate from one to another,
please checkout ``redis bgsave`` or ``redis replication`` on google.

NOTE: Package **redis** is required to use this tool.


Installation
------------

::

    pip install rdl


Usage
-----

::

    usage: rdl [-n N] [-h HOST] [-p PORT] [-a AUTH] [-f] [--ignore-none-value]
               [--help] [--version]
               ACTION FILE

    Redis dump-load tool.

    positional arguments:
      ACTION                `dump` or `load`.
      FILE                  if action is dump, then its output file, if actions is
                            load, then its source file.

    optional arguments:
      -n N                  Number of database to process.
      -h HOST, --host HOST  Redis host
      -p PORT, --port PORT  Redis port
      -a AUTH, --auth AUTH  Redis password
      -f, --flushdb         Force or flush database before load
      --ignore-none-value   Ignore None when dumping db, by default it will raise
                            ValueError if DUMP result is None
      --help                show this help message and exit
      --version             show program's version number and exit


Example
-------

Dump database 1 to file ``redis.dump``::

    $ ./rdl.py dump redis.dump -n 1

Load to database 3 from file ``redis.dump``::

    $ ./rdl.py load redis.dump -n 3 -f
