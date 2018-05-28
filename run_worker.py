import redis
from rq import Connection, Queue
from settings import REDIS_URL
from worker.model import ModelWorker


listen = ['default']

conn = redis.from_url(REDIS_URL)


if __name__ == '__main__':
    with Connection(conn):
        worker = ModelWorker(map(Queue, listen))
        worker.work()
