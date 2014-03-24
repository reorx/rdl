#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import redis
import base64
import argparse


BUF_LIMIT = 1024 * 64  # 64K


def write(file_name, buf, initial=False):
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


def dump(file_name, n):
    db = redis.StrictRedis(db=n)
    print 'Use database %s' % n

    buf = ''
    loop = 0

    write(file_name, buf, True)

    for k in db.keys():
        v = db.dump(k)
        line = '%s\t%s\n' % (k, base64.b64encode(v))
        buf += line
        loop += 1

        if loop % BUF_LIMIT == 0:
            write(file_name, buf)
            # Clear buf
            buf = ''
            print_loop(loop)

    # In case of not reach limit
    if buf:
        write(file_name, buf)

    print_loop(loop, False)


def load(file_name, n, f):
    db = redis.StrictRedis(db=n)
    print 'Use database %s' % n

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
    parser = argparse.ArgumentParser(description="Redis dump-load tool.")
    parser.add_argument('action', metavar="ACTION", type=str, choices=['dump', 'load'], help="`dump` or `load`.")
    parser.add_argument('file_name', metavar="FILE", type=str, help="if action is dump, then its output file, if actions is load, then its source file.")
    parser.add_argument('-n', type=int, default=0, help="Number of database to process.")
    parser.add_argument('-f', action='store_true', help="Force or flush database before load")

    args = parser.parse_args()

    if 'dump' == args.action:
        dump(args.file_name, args.n)
    else:  # load
        load(args.file_name, args.n, args.f)


if __name__ == '__main__':
    main()
