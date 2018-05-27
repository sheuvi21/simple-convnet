import redis
from rq import Connection, Worker, Queue
from settings import REDIS_URL


listen = ['default']

conn = redis.from_url(REDIS_URL)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
