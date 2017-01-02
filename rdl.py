#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import redis
import base64
import argparse


BUF_LIMIT = 1024 * 64  # 64K


def write_file(file_name, buf, initial=False):
    if initial:
        mode = 'w'
        if os.path.exists(file_name):
            print 'Warning: %s will be covered!' % file_name
    else:
        mode = 'a'

    with open(file_name, mode) as f:
        f.write(buf)


def print_loop(loop, clear=True):
    s = 'processed: %s' % loop

    if clear:
        sys.stdout.write(s)
        sys.stdout.flush()
        sys.stdout.write(len(s) * '\b')
    else:
        print s


def get_client(n, host=None, port=None, password=None):
    if hasattr(redis, 'StrictRedis'):
        client_class = redis.StrictRedis
    else:
        # Backward compatibility
        client_class = redis.Redis
    kwargs = {}
    if host:
        kwargs['host'] = host
    if port:
        kwargs['port'] = port
    if password:
        kwargs['password'] = password
    db = client_class(db=n, **kwargs)
    print 'Use database %s:%s, db %s' % (host or '<default host>', port or '<default port>', n)
    # TODO show db info
    return db


def dump(file_name, db):
    buf = ''
    loop = 0

    write_file(file_name, buf, True)

    for k in db.keys():
        v = db.dump(k)
        line = '%s\t%s\n' % (k, base64.b64encode(v))
        buf += line
        loop += 1

        if loop % BUF_LIMIT == 0:
            write_file(file_name, buf)
            # Clear buf
            buf = ''
            print_loop(loop)

    # In case of not reach limit
    if buf:
        write_file(file_name, buf)

    print_loop(loop, False)


def load(file_name, db, f):
    if f:
        print 'Flush database!'
        db.flushdb()

    with open(file_name, 'r') as f:
        loop = 0
        for line in f:
            k, v = tuple(line.split('\t'))
            v = base64.b64decode(v)
            db.restore(k, 0, v)

            loop += 1
            if loop % BUF_LIMIT == 0:
                print_loop(loop)

        print_loop(loop, False)


def main():
    parser = argparse.ArgumentParser(description="Redis dump-load tool.", add_help=False)
    parser.add_argument('action', metavar="ACTION", type=str, choices=['dump', 'load'], help="`dump` or `load`.")
    parser.add_argument('file_name', metavar="FILE", type=str, help="if action is dump, then its output file, if actions is load, then its source file.")
    parser.add_argument('-n', type=int, default=0, help="Number of database to process.")
    parser.add_argument('-h', type=str, help="Redis host")
    parser.add_argument('-p', type=int, help="Redis port")
    parser.add_argument('-P', type=str, help="Redis password")
    parser.add_argument('-f', action='store_true', help="Force or flush database before load")
    parser.add_argument('--help', action='help', help="show this help message and exit")

    args = parser.parse_args()

    db = get_client(args.n, args.h, args.p, args.P)

    if 'dump' == args.action:
        dump(args.file_name, db)
    else:  # load
        load(args.file_name, db, args.f)


if __name__ == '__main__':
    main()
