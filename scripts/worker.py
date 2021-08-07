#!/usr/bin/env python

import os
import sys
import zlib
import json

from rq import Connection, Worker, Queue
from redis import StrictRedis

sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir, 'apps'))


class JSONSerializer:
    @staticmethod
    def dumps(*args, **kwargs):
        return json.dumps(*args, **kwargs).encode('utf-8')

    @staticmethod
    def loads(s, *args, **kwargs):
        return json.loads(s.decode('utf-8'), *args, **kwargs)


class ZlibSerializer:
    @staticmethod
    def dumps(*args, **kwargs):
        return zlib.compress(json.dumps(*args, **kwargs).encode('utf-8'))

    @staticmethod
    def loads(s, *args, **kwargs):
        return json.loads(zlib.decompress(s).decode('utf-8'), *args, **kwargs)


serializer = ZlibSerializer

with Connection():
    conn = StrictRedis(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT')),
        db=int(os.getenv('REDIS_DB')))

    queue = Queue(
        os.getenv('REDIS_QUEUE'),
        connection=conn,
        serializer=serializer,
    )

    qs = [queue]

    w = Worker(
        qs,
        connection=conn,
        serializer=serializer,
    )
    w.work()
