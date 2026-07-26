from rq import Worker, Queue
from redis import Redis
from config import REDIS_HOST, REDIS_PORT, QUEUE_NAME

redis = Redis(host=REDIS_HOST, port=REDIS_PORT)
queue = Queue(QUEUE_NAME, connection=redis)

if __name__ == "__main__":
    worker = Worker(queues=[queue], connection=redis)
    worker.work()
