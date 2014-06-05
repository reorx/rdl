rdl - Redis dump-load tool
==========================

This tool is made specially for dump & load certain database of a redis server,
if you want to dump whole redis or replicate from one to another,
please checkout ``redis bgsave`` or ``redis replication`` on google.

NOTE: Package **redis** is required to use this tool.

Usage
-----

::

    usage: rdl.py [-n N] [-h H] [-p P] [-f] [--help] ACTION FILE

    Redis dump-load tool.

    positional arguments:
      ACTION  `dump` or `load`.
      FILE    if action is dump, then its output file, if actions is load, then
              its source file.

    optional arguments:
      -n N    Number of database to process.
      -h H    Redis host
      -p P    Redis port
      -f      Force or flush database before load
      --help  show this help message and exit


Example
-------

Dump database 1 to file ``redis.dump``::

    $ ./rdl.py dump redis.dump -n 1

Load to database 3 from file ``redis.dump``::

    $ ./rdl.py load redis.dump -n 3 -f
