import os
import base64
import tempfile
import itertools
import subprocess

import six
import pytest
from rdl import get_client


@pytest.fixture
def redisconf():
    class confobj:
        host = os.environ.get('REDIS_HOST', None)
        port = os.environ.get('REDIS_PORT', None)
        auth = os.environ.get('REDIS_AUTH', None)
        db = os.environ.get('REDIS_DB', 0)

        def args(self):
            l = []
            if self.host:
                l.extend(['-h', self.hsot])
            if self.port:
                l.extend(['-p', self.port])
            if self.auth:
                l.extend(['-a', self.auth])
            return l

        def client(self):
            return get_client(self.db, self.host, self.port, self.auth)

    return confobj()


@pytest.fixture
def kvd():
    return [
        (b'a:1', b'1', b'\x00\xc0\x01\b\x00\x9fU\x0b\tx\x18\x9b\xc4'),
        (b'a:2', b'2', b'\x00\xc0\x02\b\x006\x8f\\\x03Q\xcd\xf4\xf3'),
        (b'a:3', b'3', b'\x00\xc0\x03\b\x00\x88\xb7\x1c\xcdx\x9c\xe6\a'),
    ]


def generate_result(kvd_):
    r = b''
    for k, _, d in kvd_:
        r += b'%s\t%s\n' % (k, base64.b64encode(d))
    return r


def test_rdl_dump(redisconf, kvd):
    # get client
    c = redisconf.client()
    c.flushdb()
    for k, v, _ in kvd:
        c.set(k, v)
    results_combinations = [generate_result(kvd_) for kvd_ in itertools.permutations(kvd, 3)]
    print(results_combinations)

    # form cmd
    cmd = ['rdl']
    cmd.extend(redisconf.args())
    _, dump_file = tempfile.mkstemp()
    cmd.extend(['dump', dump_file])

    # run cmd
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    # asserts
    assert p.returncode == 0, '{} failed: {}, {}'.format(cmd, out, err)
    with open(dump_file, 'rb') as f:
        assert f.read() in results_combinations
